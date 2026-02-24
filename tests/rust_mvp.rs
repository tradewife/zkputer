use std::sync::Arc;
use std::time::Duration;
use anyhow::{anyhow, Result};
use async_trait::async_trait;
use serde_json::Value;
use zkputer::adapters::{SyntheticVenueAdapter, VenueAdapter};
use zkputer::models::{
    ClaimType, NonProvableReason, ProofBackend, ProofMetadata, ProofRequest, ReceiptStatus, Venue,
};
use zkputer::policy::PolicyEngine;
use zkputer::prover::{FallbackProver, PicoMvpProver, ProverBackend, Sp1MvpProver};
use zkputer::templates::{
    build_request_from_template, TEMPLATE_ORDER_PLACEMENT_VERIFICATION,
};
use zkputer::verifier::OffchainVerifier;
use zkputer::ReceiptEngine;

fn engine_with_prover(prover: Arc<dyn ProverBackend>) -> ReceiptEngine {
    let adapters: Vec<Arc<dyn VenueAdapter>> = vec![
        Arc::new(SyntheticVenueAdapter::new(Venue::Hyperliquid)),
        Arc::new(SyntheticVenueAdapter::new(Venue::Base)),
        Arc::new(SyntheticVenueAdapter::new(Venue::Solana)),
        Arc::new(SyntheticVenueAdapter::new(Venue::Polymarket)),
    ];
    ReceiptEngine::new(
        adapters,
        PolicyEngine::new(None).expect("policy should load"),
        prover,
        OffchainVerifier::default(),
    )
}

fn engine() -> ReceiptEngine {
    engine_with_prover(Arc::new(Sp1MvpProver))
}

#[derive(Debug)]
struct AlwaysFailProver;

#[async_trait]
impl ProverBackend for AlwaysFailProver {
    fn backend_name(&self) -> ProofBackend {
        ProofBackend::SP1
    }

    async fn prove(&self, _public_inputs: &Value) -> Result<ProofMetadata> {
        Err(anyhow!("forced primary prover failure"))
    }
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

#[tokio::test]
async fn fallback_prover_uses_pico_when_primary_fails() {
    let engine = engine_with_prover(Arc::new(FallbackProver::new(
        Arc::new(AlwaysFailProver),
        Arc::new(PicoMvpProver),
    )));
    let receipt_id = engine
        .submit(ProofRequest {
            venue: Venue::Polymarket,
            claim_type: ClaimType::ORDER_PLACED,
            account_ref: "acct-4".to_string(),
            order_ref: "order-4".to_string(),
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
    assert_eq!(receipt.proof.backend, ProofBackend::PICO);
}

#[tokio::test]
async fn template_order_placement_flow_proves() {
    let engine = engine();
    let request = build_request_from_template(
        TEMPLATE_ORDER_PLACEMENT_VERIFICATION,
        &serde_json::json!({
            "venue": "base",
            "account_ref": "acct-template-1",
            "order_ref": "order-template-1",
            "notes": "template path"
        }),
    )
    .expect("template request build");
    let receipt_id = engine.submit(request).await.expect("submit");
    let receipt = engine
        .wait_for_receipt(&receipt_id, Duration::from_secs(5))
        .await
        .expect("wait");
    assert_eq!(receipt.status, ReceiptStatus::PROVED);
    assert_eq!(
        receipt.provenance.evidence_items.is_empty(),
        false,
        "evidence should be present"
    );
}
