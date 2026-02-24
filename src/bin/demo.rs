use std::sync::Arc;
use std::time::Duration;
use zkputer::adapters::SyntheticVenueAdapter;
use zkputer::models::{ClaimType, ProofRequest, Venue};
use zkputer::policy::PolicyEngine;
use zkputer::prover::{build_mvp_prover, ProverStrategy};
use zkputer::verifier::OffchainVerifier;
use zkputer::ReceiptEngine;

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let prover_strategy_env = std::env::var("ZKPUTER_PROVER_STRATEGY").ok();
    let prover_strategy = ProverStrategy::from_env(prover_strategy_env.as_deref());
    let adapters: Vec<Arc<dyn zkputer::adapters::VenueAdapter>> = vec![
        Arc::new(SyntheticVenueAdapter::new(Venue::Hyperliquid)),
        Arc::new(SyntheticVenueAdapter::new(Venue::Base)),
        Arc::new(SyntheticVenueAdapter::new(Venue::Solana)),
        Arc::new(SyntheticVenueAdapter::new(Venue::Polymarket)),
    ];
    let engine = ReceiptEngine::new(
        adapters,
        PolicyEngine::new(None)?,
        build_mvp_prover(prover_strategy),
        OffchainVerifier::default(),
    );
    let request = ProofRequest {
        venue: Venue::Hyperliquid,
        claim_type: ClaimType::ORDER_PLACED,
        account_ref: "acct-demo-01".to_string(),
        order_ref: "ord-abc-001".to_string(),
        execution_ref: None,
        payload: serde_json::json!({}),
    };
    let receipt_id = engine.submit(request).await?;
    let receipt = engine
        .wait_for_receipt(&receipt_id, Duration::from_secs(5))
        .await?;
    println!("{}", serde_json::to_string_pretty(&receipt)?);
    Ok(())
}
