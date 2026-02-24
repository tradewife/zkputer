use crate::models::{hash_json, ProofBackend, ProofMetadata, VerificationMode};
use anyhow::{anyhow, Result};
use async_trait::async_trait;
use serde_json::Value;
use std::sync::Arc;

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

#[derive(Debug, Clone)]
pub struct PicoMvpProver;

#[async_trait]
impl ProverBackend for PicoMvpProver {
    fn backend_name(&self) -> ProofBackend {
        ProofBackend::PICO
    }

    async fn prove(&self, public_inputs: &Value) -> Result<ProofMetadata> {
        let public_inputs_hash = hash_json(public_inputs);
        Ok(ProofMetadata {
            backend: ProofBackend::PICO,
            circuit_id: "trade-receipt-pico".to_string(),
            circuit_version: "v0.1.0".to_string(),
            verifier_key_id: "pico-vk-001".to_string(),
            verifier_key_hash: hash_json(&serde_json::json!({
                "backend": "PICO",
                "verifier_key": "001"
            })),
            public_inputs_hash: public_inputs_hash.clone(),
            verification_mode: VerificationMode::OFFCHAIN,
            proof_artifact_ref: Some(format!("pico://receipt/{}", public_inputs_hash)),
            anchored_root_ref: None,
        })
    }
}

pub struct FallbackProver {
    primary: Arc<dyn ProverBackend>,
    secondary: Arc<dyn ProverBackend>,
}

impl FallbackProver {
    pub fn new(primary: Arc<dyn ProverBackend>, secondary: Arc<dyn ProverBackend>) -> Self {
        Self { primary, secondary }
    }
}

#[async_trait]
impl ProverBackend for FallbackProver {
    fn backend_name(&self) -> ProofBackend {
        self.primary.backend_name()
    }

    async fn prove(&self, public_inputs: &Value) -> Result<ProofMetadata> {
        match self.primary.prove(public_inputs).await {
            Ok(proof) => Ok(proof),
            Err(primary_err) => self.secondary.prove(public_inputs).await.map_err(|secondary_err| {
                anyhow!(
                    "primary backend {:?} failed: {}; fallback backend {:?} failed: {}",
                    self.primary.backend_name(),
                    primary_err,
                    self.secondary.backend_name(),
                    secondary_err
                )
            }),
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ProverStrategy {
    Sp1Only,
    PicoOnly,
    Sp1WithPicoFallback,
}

impl ProverStrategy {
    pub fn from_env(raw: Option<&str>) -> Self {
        match raw.unwrap_or("sp1").trim().to_ascii_lowercase().as_str() {
            "pico" => Self::PicoOnly,
            "sp1_with_pico_fallback" | "sp1+pico" => Self::Sp1WithPicoFallback,
            _ => Self::Sp1Only,
        }
    }
}

pub fn build_mvp_prover(strategy: ProverStrategy) -> Arc<dyn ProverBackend> {
    match strategy {
        ProverStrategy::Sp1Only => Arc::new(Sp1MvpProver),
        ProverStrategy::PicoOnly => Arc::new(PicoMvpProver),
        ProverStrategy::Sp1WithPicoFallback => {
            Arc::new(FallbackProver::new(Arc::new(Sp1MvpProver), Arc::new(PicoMvpProver)))
        }
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
