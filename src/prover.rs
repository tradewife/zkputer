use crate::models::{hash_json, ProofBackend, ProofMetadata, VerificationMode};
use anyhow::Result;
use async_trait::async_trait;
use serde_json::Value;

#[async_trait]
pub trait ProverBackend: Send + Sync {
    fn backend_name(&self) -> ProofBackend;
    async fn prove(&self, public_inputs: &Value) -> Result<ProofMetadata>;
}

#[derive(Debug, Clone)]
pub struct Sp1MvpProver;

#[async_trait]
impl ProverBackend for Sp1MvpProver {
    fn backend_name(&self) -> ProofBackend {
        ProofBackend::SP1
    }

    async fn prove(&self, public_inputs: &Value) -> Result<ProofMetadata> {
        let public_inputs_hash = hash_json(public_inputs);
        Ok(ProofMetadata {
            backend: ProofBackend::SP1,
            circuit_id: "trade-receipt-sp1".to_string(),
            circuit_version: "v0.1.0".to_string(),
            verifier_key_id: "sp1-vk-001".to_string(),
            verifier_key_hash: hash_json(&serde_json::json!({
                "backend": "SP1",
                "verifier_key": "001"
            })),
            public_inputs_hash: public_inputs_hash.clone(),
            verification_mode: VerificationMode::OFFCHAIN,
            proof_artifact_ref: Some(format!("boundless://sp1/{}", public_inputs_hash)),
            anchored_root_ref: None,
        })
    }
}

pub fn no_proof_metadata() -> ProofMetadata {
    ProofMetadata {
        backend: ProofBackend::NONE,
        circuit_id: "none".to_string(),
        circuit_version: "none".to_string(),
        verifier_key_id: "none".to_string(),
        verifier_key_hash: format!("0x{}", "0".repeat(64)),
        public_inputs_hash: format!("0x{}", "0".repeat(64)),
        verification_mode: VerificationMode::OFFCHAIN,
        proof_artifact_ref: None,
        anchored_root_ref: None,
    }
}
