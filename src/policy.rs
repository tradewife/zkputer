use crate::models::{ClaimType, EvidenceBundle, NonProvableReason, Venue};
use anyhow::{Context, Result};
use serde_json::Value;
use std::path::{Path, PathBuf};

#[derive(Debug, Clone)]
pub struct PolicyDecision {
    pub ok: bool,
    pub reason: Option<NonProvableReason>,
    pub details: String,
}

#[derive(Debug, Clone)]
pub struct PolicyEngine {
    claim_taxonomy: Value,
    source_precedence: Value,
}

impl PolicyEngine {
    pub fn new(repo_root: Option<&Path>) -> Result<Self> {
        let root = repo_root
            .map(PathBuf::from)
            .unwrap_or_else(|| PathBuf::from(env!("CARGO_MANIFEST_DIR")));
        let spec_dir = root.join("spec");
        let claim_taxonomy = read_json(&spec_dir.join("claim-taxonomy.json"))?;
        let source_precedence = read_json(&spec_dir.join("source-precedence.json"))?;
        Ok(Self {
            claim_taxonomy,
            source_precedence,
        })
    }

    pub fn source_precedence_version(&self) -> String {
        self.source_precedence
            .get("version")
            .and_then(|v| v.as_str())
            .unwrap_or("unknown")
            .to_string()
    }

    pub fn policy_id(&self) -> String {
        "default-v0.1.0".to_string()
    }

    pub fn finality_rule_id(&self) -> String {
        "venue-default-finality-v0.1.0".to_string()
    }

    pub fn evaluate(&self, venue: Venue, claim_type: ClaimType, bundle: &EvidenceBundle) -> PolicyDecision {
        if !bundle.conflicts.is_empty() {
            return PolicyDecision {
                ok: false,
                reason: Some(NonProvableReason::EVIDENCE_CONFLICT),
                details: format!("Conflicting evidence entries detected: {}", bundle.conflicts.join(", ")),
            };
        }

        if bundle.items.is_empty() {
            return PolicyDecision {
                ok: false,
                reason: Some(NonProvableReason::EVIDENCE_MISSING),
                details: "No evidence artifacts were collected.".to_string(),
            };
        }

        let required_tags = self.required_tags_for_claim(claim_type);
        let missing_tags: Vec<String> = required_tags
            .into_iter()
            .filter(|tag| !bundle.observed_tags.contains(tag))
            .collect();
        if !missing_tags.is_empty() {
            return PolicyDecision {
                ok: false,
                reason: Some(NonProvableReason::EVIDENCE_MISSING),
                details: format!("Missing required evidence tags: {}", missing_tags.join(", ")),
            };
        }

        let preferred = self.preferred_sources(venue, claim_type);
        let observed: Vec<&str> = bundle.items.iter().map(|i| i.source_kind.as_str()).collect();
        if !preferred.is_empty() && !preferred.iter().any(|p| observed.contains(&p.as_str())) {
            return PolicyDecision {
                ok: false,
                reason: Some(NonProvableReason::SOURCE_UNAVAILABLE),
                details: format!(
                    "No acceptable preferred source kinds observed. Expected one of: {}",
                    preferred.join(", ")
                ),
            };
        }

        PolicyDecision {
            ok: true,
            reason: None,
            details: String::new(),
        }
    }

    fn required_tags_for_claim(&self, claim_type: ClaimType) -> Vec<String> {
        let key = match claim_type {
            ClaimType::ORDER_PLACED => "ORDER_PLACED",
            ClaimType::TRADE_EXECUTED => "TRADE_EXECUTED",
        };
        self.claim_taxonomy
            .get("claim_types")
            .and_then(|v| v.get(key))
            .and_then(|v| v.get("required_evidence_tags_all"))
            .and_then(|v| v.as_array())
            .map(|arr| {
                arr.iter()
                    .filter_map(|v| v.as_str().map(|s| s.to_string()))
                    .collect()
            })
            .unwrap_or_default()
    }

    fn preferred_sources(&self, venue: Venue, claim_type: ClaimType) -> Vec<String> {
        let venue_key = match venue {
            Venue::Hyperliquid => "hyperliquid",
            Venue::Base => "base",
            Venue::Solana => "solana",
            Venue::Polymarket => "polymarket",
        };
        let list_key = match claim_type {
            ClaimType::ORDER_PLACED => "order_placed_sources_preferred",
            ClaimType::TRADE_EXECUTED => "trade_executed_sources_preferred",
        };
        self.source_precedence
            .get("venues")
            .and_then(|v| v.get(venue_key))
            .and_then(|v| v.get(list_key))
            .and_then(|v| v.as_array())
            .map(|arr| {
                arr.iter()
                    .filter_map(|v| v.as_str().map(|s| s.to_string()))
                    .collect()
            })
            .unwrap_or_default()
    }
}

fn read_json(path: &Path) -> Result<Value> {
    let text = std::fs::read_to_string(path).with_context(|| format!("failed to read {}", path.display()))?;
    let parsed: Value =
        serde_json::from_str(&text).with_context(|| format!("failed to parse json {}", path.display()))?;
    Ok(parsed)
}
