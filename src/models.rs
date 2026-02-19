use chrono::Utc;
use serde::{Deserialize, Serialize};
use serde_json::Value;
use sha2::{Digest, Sha256};
use std::collections::HashSet;
use uuid::Uuid;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum Venue {
    Hyperliquid,
    Base,
    Solana,
    Polymarket,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[allow(non_camel_case_types)]
pub enum ClaimType {
    ORDER_PLACED,
    TRADE_EXECUTED,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[allow(non_camel_case_types)]
pub enum ReceiptStatus {
    PENDING,
    PROVED,
    NON_PROVABLE,
    INVALIDATED,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[allow(non_camel_case_types)]
pub enum NonProvableReason {
    EVIDENCE_MISSING,
    EVIDENCE_CONFLICT,
    SOURCE_UNAVAILABLE,
    FINALITY_TIMEOUT,
    POLICY_VIOLATION,
    SCHEMA_INVALID,
    UNSUPPORTED_VENUE_CLAIM,
    PROOF_FAILURE,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[allow(non_camel_case_types)]
pub enum VerificationMode {
    OFFCHAIN,
    ONCHAIN_ANCHORED,
    OFFCHAIN_AND_ANCHORED,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum ProofBackend {
    SP1,
    PICO,
    NONE,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EvidenceItem {
    pub source_id: String,
    pub source_kind: String,
    pub artifact_ref: String,
    pub artifact_hash: String,
    pub observed_at: String,
    #[serde(default)]
    pub tags: Vec<String>,
}

#[derive(Debug, Clone)]
pub struct EvidenceBundle {
    pub items: Vec<EvidenceItem>,
    pub observed_tags: HashSet<String>,
    pub conflicts: Vec<String>,
    pub finality_observed_at: Option<String>,
}

impl EvidenceBundle {
    pub fn evidence_root(&self) -> String {
        let mut leaves: Vec<&String> = self.items.iter().map(|i| &i.artifact_hash).collect();
        leaves.sort();
        hash_json(&serde_json::json!({ "leaves": leaves }))
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ProofRequest {
    pub venue: Venue,
    pub claim_type: ClaimType,
    pub account_ref: String,
    pub order_ref: String,
    pub execution_ref: Option<String>,
    #[serde(default)]
    pub payload: Value,
}

#[derive(Debug, Clone)]
pub struct ExecutionAck {
    pub accepted: bool,
    pub venue_order_ref: String,
    pub acceptance_artifact_ref: String,
    pub acceptance_artifact_hash: String,
    pub accepted_at: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TruthClaim {
    pub r#type: ClaimType,
    pub statement: String,
    pub claim_hash: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Subject {
    pub venue: Venue,
    pub account_ref: String,
    pub order_ref: String,
    pub execution_ref: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PolicyContext {
    pub policy_id: String,
    pub finality_rule_id: String,
    pub source_precedence_version: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Provenance {
    pub evidence_root: String,
    pub evidence_items: Vec<EvidenceItem>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Timing {
    pub created_at: String,
    pub updated_at: String,
    pub execution_observed_at: Option<String>,
    pub finality_observed_at: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ProofMetadata {
    pub backend: ProofBackend,
    pub circuit_id: String,
    pub circuit_version: String,
    pub verifier_key_id: String,
    pub verifier_key_hash: String,
    pub public_inputs_hash: String,
    pub verification_mode: VerificationMode,
    pub proof_artifact_ref: Option<String>,
    pub anchored_root_ref: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct NonProvable {
    pub reason_code: NonProvableReason,
    pub details: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Integrity {
    pub schema_hash: String,
    pub receipt_hash: String,
    pub signer: String,
    pub signature: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ZKReceipt {
    pub receipt_id: String,
    pub version: String,
    pub status: ReceiptStatus,
    pub claim: TruthClaim,
    pub subject: Subject,
    pub policy: PolicyContext,
    pub provenance: Provenance,
    pub timing: Timing,
    pub proof: ProofMetadata,
    pub integrity: Integrity,
    pub non_provable: Option<NonProvable>,
}

pub fn now_iso() -> String {
    Utc::now().to_rfc3339_opts(chrono::SecondsFormat::Millis, true)
}

pub fn new_receipt_id() -> String {
    Uuid::new_v4().to_string()
}

pub fn hash_str(input: &str) -> String {
    let mut hasher = Sha256::new();
    hasher.update(input.as_bytes());
    format!("0x{}", hex::encode(hasher.finalize()))
}

pub fn hash_json(value: &impl Serialize) -> String {
    let serialized = serde_json::to_string(value).unwrap_or_else(|_| "{}".to_string());
    hash_str(&serialized)
}
