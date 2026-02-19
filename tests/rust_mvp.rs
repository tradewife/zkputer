use std::sync::Arc;
use std::time::Duration;
use zkputer::adapters::{SyntheticVenueAdapter, VenueAdapter};
use zkputer::models::{ClaimType, NonProvableReason, ProofRequest, ReceiptStatus, Venue};
use zkputer::policy::PolicyEngine;
use zkputer::prover::Sp1MvpProver;
use zkputer::verifier::OffchainVerifier;
use zkputer::ReceiptEngine;

fn engine() -> ReceiptEngine {
    let adapters: Vec<Arc<dyn VenueAdapter>> = vec![
        Arc::new(SyntheticVenueAdapter::new(Venue::Hyperliquid)),
        Arc::new(SyntheticVenueAdapter::new(Venue::Base)),
        Arc::new(SyntheticVenueAdapter::new(Venue::Solana)),
        Arc::new(SyntheticVenueAdapter::new(Venue::Polymarket)),
    ];
    ReceiptEngine::new(
        adapters,
        PolicyEngine::new(None).expect("policy should load"),
        Arc::new(Sp1MvpProver),
        OffchainVerifier::default(),
    )
}

#[tokio::test]
async fn order_placed_proves() {
    let engine = engine();
    let receipt_id = engine
        .submit(ProofRequest {
            venue: Venue::Base,
            claim_type: ClaimType::ORDER_PLACED,
            account_ref: "acct-1".to_string(),
            order_ref: "order-1".to_string(),
            execution_ref: None,
            payload: serde_json::json!({}),
        })
        .await
        .expect("submit");
    let receipt = engine
        .wait_for_receipt(&receipt_id, Duration::from_secs(5))
        .await
        .expect("wait");
    assert_eq!(receipt.status, ReceiptStatus::PROVED);
}

#[tokio::test]
async fn trade_executed_missing_execution_ref_non_provable() {
    let engine = engine();
    let receipt_id = engine
        .submit(ProofRequest {
            venue: Venue::Solana,
            claim_type: ClaimType::TRADE_EXECUTED,
            account_ref: "acct-2".to_string(),
            order_ref: "order-2".to_string(),
            execution_ref: None,
            payload: serde_json::json!({}),
        })
        .await
        .expect("submit");
    let receipt = engine
        .wait_for_receipt(&receipt_id, Duration::from_secs(5))
        .await
        .expect("wait");
    assert_eq!(receipt.status, ReceiptStatus::NON_PROVABLE);
    assert_eq!(
        receipt
            .non_provable
            .as_ref()
            .expect("non provable present")
            .reason_code,
        NonProvableReason::EVIDENCE_MISSING
    );
}

#[tokio::test]
async fn conflicting_evidence_non_provable() {
    let engine = engine();
    let receipt_id = engine
        .submit(ProofRequest {
            venue: Venue::Hyperliquid,
            claim_type: ClaimType::ORDER_PLACED,
            account_ref: "acct-3".to_string(),
            order_ref: "order-3".to_string(),
            execution_ref: None,
            payload: serde_json::json!({"simulate_conflict": true}),
        })
        .await
        .expect("submit");
    let receipt = engine
        .wait_for_receipt(&receipt_id, Duration::from_secs(5))
        .await
        .expect("wait");
    assert_eq!(receipt.status, ReceiptStatus::NON_PROVABLE);
    assert_eq!(
        receipt
            .non_provable
            .as_ref()
            .expect("non provable present")
            .reason_code,
        NonProvableReason::EVIDENCE_CONFLICT
    );
}
