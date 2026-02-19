use crate::adapters::base::VenueAdapter;
use crate::models::{
    now_iso, hash_json, ClaimType, EvidenceBundle, EvidenceItem, ExecutionAck, ProofRequest, Venue,
};
use anyhow::Result;
use async_trait::async_trait;
use std::collections::HashSet;

#[derive(Debug)]
pub struct SyntheticVenueAdapter {
    venue: Venue,
}

fn venue_slug(venue: Venue) -> &'static str {
    match venue {
        Venue::Hyperliquid => "hyperliquid",
        Venue::Base => "base",
        Venue::Solana => "solana",
        Venue::Polymarket => "polymarket",
    }
}

impl SyntheticVenueAdapter {
    pub fn new(venue: Venue) -> Self {
        Self { venue }
    }
}

fn acceptance_source_kind(venue: Venue) -> &'static str {
    match venue {
        Venue::Hyperliquid => "venue_signed_attestation",
        _ => "canonical_chain_state",
    }
}

#[async_trait]
impl VenueAdapter for SyntheticVenueAdapter {
    fn venue(&self) -> Venue {
        self.venue
    }

    async fn acknowledge(&self, request: &ProofRequest) -> Result<ExecutionAck> {
        let accepted_at = now_iso();
        let artifact_ref = format!("{}://ack/{}", venue_slug(self.venue), request.order_ref);
        let artifact_hash = hash_json(&serde_json::json!({
            "venue": venue_slug(self.venue),
            "order_ref": request.order_ref,
            "accepted_at": accepted_at,
            "kind": "acknowledgement"
        }));
        Ok(ExecutionAck {
            accepted: true,
            venue_order_ref: request.order_ref.clone(),
            acceptance_artifact_ref: artifact_ref,
            acceptance_artifact_hash: artifact_hash,
            accepted_at,
        })
    }

    async fn collect_evidence(&self, request: &ProofRequest, ack: &ExecutionAck) -> Result<EvidenceBundle> {
        let mut observed_tags = HashSet::from([
            "order_identity".to_string(),
            "submission_timestamp".to_string(),
            "venue_acceptance_artifact".to_string(),
        ]);
        let mut conflicts = Vec::new();
        let payload = &request.payload;
        if payload.get("simulate_conflict").and_then(|v| v.as_bool()).unwrap_or(false) {
            conflicts.push("source_value_mismatch".to_string());
        }

        let primary = EvidenceItem {
            source_id: format!("{}-primary", venue_slug(self.venue)),
            source_kind: acceptance_source_kind(self.venue).to_string(),
            artifact_ref: ack.acceptance_artifact_ref.clone(),
            artifact_hash: ack.acceptance_artifact_hash.clone(),
            observed_at: ack.accepted_at.clone(),
            tags: vec![
                "order_identity".to_string(),
                "submission_timestamp".to_string(),
                "venue_acceptance_artifact".to_string(),
            ],
        };

        let shadow = EvidenceItem {
            source_id: format!("{}-api", venue_slug(self.venue)),
            source_kind: "venue_api_unsigned".to_string(),
            artifact_ref: format!("{}://api/order/{}", venue_slug(self.venue), request.order_ref),
            artifact_hash: hash_json(&serde_json::json!({
                "venue": venue_slug(self.venue),
                "api_order_ref": request.order_ref
            })),
            observed_at: now_iso(),
            tags: vec!["order_identity".to_string(), "submission_timestamp".to_string()],
        };

        let mut items = vec![primary, shadow];
        let mut finality_observed_at = None;

        if request.claim_type == ClaimType::TRADE_EXECUTED {
            if let Some(execution_ref) = &request.execution_ref {
                observed_tags.insert("execution_identity".to_string());
                observed_tags.insert("execution_timestamp".to_string());
                observed_tags.insert("execution_artifact".to_string());
                items.push(EvidenceItem {
                    source_id: format!("{}-execution", venue_slug(self.venue)),
                    source_kind: acceptance_source_kind(self.venue).to_string(),
                    artifact_ref: format!("{}://execution/{}", venue_slug(self.venue), execution_ref),
                    artifact_hash: hash_json(&serde_json::json!({
                        "venue": venue_slug(self.venue),
                        "order_ref": request.order_ref,
                        "execution_ref": execution_ref
                    })),
                    observed_at: now_iso(),
                    tags: vec![
                        "execution_identity".to_string(),
                        "execution_timestamp".to_string(),
                        "execution_artifact".to_string(),
                    ],
                });
                finality_observed_at = Some(now_iso());
            }
        }

        if let Some(missing_tags) = payload.get("missing_tags").and_then(|v| v.as_array()) {
            for tag in missing_tags.iter().filter_map(|v| v.as_str()) {
                observed_tags.remove(tag);
            }
        }

        Ok(EvidenceBundle {
            items,
            observed_tags,
            conflicts,
            finality_observed_at,
        })
    }
}
