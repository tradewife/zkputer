use crate::models::{hash_json, ClaimType, ProofBackend, ReceiptStatus, Venue, ZKReceipt};

#[derive(Debug, Default, Clone)]
pub struct OffchainVerifier;

impl OffchainVerifier {
    pub async fn verify(&self, receipt: &ZKReceipt) -> bool {
        if receipt.status != ReceiptStatus::PROVED {
            return false;
        }
        if receipt.proof.backend == ProofBackend::NONE {
            return false;
        }
        let venue = match receipt.subject.venue {
            Venue::Hyperliquid => "hyperliquid",
            Venue::Base => "base",
            Venue::Solana => "solana",
            Venue::Polymarket => "polymarket",
        };
        let claim_type = match receipt.claim.r#type {
            ClaimType::ORDER_PLACED => "ORDER_PLACED",
            ClaimType::TRADE_EXECUTED => "TRADE_EXECUTED",
        };
        let expected = hash_json(&serde_json::json!({
            "claim_hash": receipt.claim.claim_hash,
            "evidence_root": receipt.provenance.evidence_root,
            "venue": venue,
            "claim_type": claim_type
        }));
        expected == receipt.proof.public_inputs_hash
    }
}
