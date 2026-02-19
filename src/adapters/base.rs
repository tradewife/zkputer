use crate::models::{EvidenceBundle, ExecutionAck, ProofRequest, Venue};
use anyhow::Result;
use async_trait::async_trait;
fn venue_slug(venue: Venue) -> &'static str {
    match venue {
        Venue::Hyperliquid => "hyperliquid",
        Venue::Base => "base",
        Venue::Solana => "solana",
        Venue::Polymarket => "polymarket",
    }
}

#[async_trait]
pub trait VenueAdapter: Send + Sync {
    fn venue(&self) -> Venue;
    async fn acknowledge(&self, request: &ProofRequest) -> Result<ExecutionAck>;
    async fn collect_evidence(&self, request: &ProofRequest, ack: &ExecutionAck) -> Result<EvidenceBundle>;

    async fn build_statement(
        &self,
        request: &ProofRequest,
        ack: &ExecutionAck,
        _bundle: &EvidenceBundle,
    ) -> Result<String> {
        let statement = if request.claim_type == crate::models::ClaimType::ORDER_PLACED {
            format!(
                "Order {} for account {} was accepted on venue {} at {}.",
                request.order_ref,
                request.account_ref,
                venue_slug(request.venue),
                ack.accepted_at
            )
        } else {
            format!(
                "Order {} for account {} was executed on venue {} with execution ref {}.",
                request.order_ref,
                request.account_ref,
                venue_slug(request.venue),
                request.execution_ref.clone().unwrap_or_else(|| "UNKNOWN".to_string())
            )
        };
        Ok(statement)
    }
}
