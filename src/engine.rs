use crate::adapters::VenueAdapter;
use crate::models::{
    hash_json, new_receipt_id, now_iso, ClaimType, Integrity, NonProvable, NonProvableReason, PolicyContext,
    ProofMetadata, ProofRequest, Provenance, ReceiptStatus, Subject, Timing, TruthClaim, Venue, ZKReceipt,
};
use crate::policy::PolicyEngine;
use crate::prover::{no_proof_metadata, ProverBackend};
use crate::verifier::OffchainVerifier;
use anyhow::{anyhow, Result};
use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::Mutex;
use tokio::task::JoinHandle;

pub struct ReceiptEngine {
    adapters: HashMap<Venue, Arc<dyn VenueAdapter>>,
    policy_engine: PolicyEngine,
    prover: Arc<dyn ProverBackend>,
    verifier: OffchainVerifier,
    signer: String,
    receipt_version: String,
    store: Arc<Mutex<HashMap<String, ZKReceipt>>>,
    tasks: Arc<Mutex<HashMap<String, JoinHandle<()>>>>,
}

impl ReceiptEngine {
    pub fn new(
        adapters: Vec<Arc<dyn VenueAdapter>>,
        policy_engine: PolicyEngine,
        prover: Arc<dyn ProverBackend>,
        verifier: OffchainVerifier,
    ) -> Self {
        let map = adapters.into_iter().map(|a| (a.venue(), a)).collect();
        Self {
            adapters: map,
            policy_engine,
            prover,
            verifier,
            signer: "zkputer-dev-signer".to_string(),
            receipt_version: "v0.1.0".to_string(),
            store: Arc::new(Mutex::new(HashMap::new())),
            tasks: Arc::new(Mutex::new(HashMap::new())),
        }
    }

    pub async fn submit(&self, request: ProofRequest) -> Result<String> {
        let receipt = self.new_pending_receipt(&request);
        let receipt_id = receipt.receipt_id.clone();
        self.store.lock().await.insert(receipt_id.clone(), receipt);

        let store = Arc::clone(&self.store);
        let tasks = Arc::clone(&self.tasks);
        let adapter = self.adapters.get(&request.venue).cloned();
        let policy_engine = self.policy_engine.clone();
        let prover = Arc::clone(&self.prover);
        let verifier = self.verifier.clone();
        let signer = self.signer.clone();
        let receipt_version = self.receipt_version.clone();
        let receipt_id_for_task = receipt_id.clone();
        let receipt_id_for_cleanup = receipt_id.clone();

        let handle = tokio::spawn(async move {
            process_receipt_task(
                store,
                adapter,
                policy_engine,
                prover,
                verifier,
                signer,
                receipt_version,
                receipt_id_for_task,
                request,
            )
            .await;
            tasks.lock().await.remove(&receipt_id_for_cleanup);
        });
        self.tasks.lock().await.insert(receipt_id.clone(), handle);
        Ok(receipt_id)
    }

    pub async fn get_receipt(&self, receipt_id: &str) -> Option<ZKReceipt> {
        self.store.lock().await.get(receipt_id).cloned()
    }

    pub async fn wait_for_receipt(&self, receipt_id: &str, timeout: std::time::Duration) -> Result<ZKReceipt> {
        let handle_opt = { self.tasks.lock().await.remove(receipt_id) };
        if let Some(handle) = handle_opt {
            tokio::time::timeout(timeout, handle).await.map_err(|_| anyhow!("timeout waiting for receipt task"))??;
        }
        self.get_receipt(receipt_id)
            .await
            .ok_or_else(|| anyhow!("unknown receipt id: {}", receipt_id))
    }

    fn new_pending_receipt(&self, request: &ProofRequest) -> ZKReceipt {
        let now = now_iso();
        let claim_hash = hash_json(&serde_json::json!({
            "venue": request.venue,
            "claim_type": request.claim_type,
            "account_ref": request.account_ref,
            "order_ref": request.order_ref,
            "execution_ref": request.execution_ref
        }));
        let claim = TruthClaim {
            r#type: request.claim_type,
            statement: "PENDING: statement unavailable until evidence collection completes".to_string(),
            claim_hash: claim_hash.clone(),
        };
        let provenance = Provenance {
            evidence_root: hash_json(&serde_json::json!({"empty": true})),
            evidence_items: vec![],
        };
        let proof = no_proof_metadata();
        let integrity = build_integrity(
            &self.signer,
            &self.receipt_version,
            ReceiptStatus::PENDING,
            &claim_hash,
            &provenance.evidence_root,
            &proof.public_inputs_hash,
        );
        ZKReceipt {
            receipt_id: new_receipt_id(),
            version: self.receipt_version.clone(),
            status: ReceiptStatus::PENDING,
            claim,
            subject: Subject {
                venue: request.venue,
                account_ref: request.account_ref.clone(),
                order_ref: request.order_ref.clone(),
                execution_ref: request.execution_ref.clone(),
            },
            policy: PolicyContext {
                policy_id: self.policy_engine.policy_id(),
                finality_rule_id: self.policy_engine.finality_rule_id(),
                source_precedence_version: self.policy_engine.source_precedence_version(),
            },
            provenance,
            timing: Timing {
                created_at: now.clone(),
                updated_at: now,
                execution_observed_at: None,
                finality_observed_at: None,
            },
            proof,
            integrity,
            non_provable: None,
        }
    }
}

async fn process_receipt_task(
    store: Arc<Mutex<HashMap<String, ZKReceipt>>>,
    adapter: Option<Arc<dyn VenueAdapter>>,
    policy_engine: PolicyEngine,
    prover: Arc<dyn ProverBackend>,
    verifier: OffchainVerifier,
    signer: String,
    receipt_version: String,
    receipt_id: String,
    request: ProofRequest,
) {
    let current = { store.lock().await.get(&receipt_id).cloned() };
    let Some(receipt) = current else { return; };

    let Some(adapter) = adapter else {
        let updated = mark_non_provable(
            receipt,
            NonProvableReason::UNSUPPORTED_VENUE_CLAIM,
            format!("No adapter registered for venue {:?}", request.venue),
            &signer,
            &receipt_version,
        );
        store.lock().await.insert(receipt_id, updated);
        return;
    };

    let ack = match adapter.acknowledge(&request).await {
        Ok(v) => v,
        Err(err) => {
            let updated = mark_non_provable(
                receipt,
                NonProvableReason::SOURCE_UNAVAILABLE,
                err.to_string(),
                &signer,
                &receipt_version,
            );
            store.lock().await.insert(receipt_id, updated);
            return;
        }
    };

    let bundle = match adapter.collect_evidence(&request, &ack).await {
        Ok(v) => v,
        Err(err) => {
            let updated = mark_non_provable(
                receipt,
                NonProvableReason::SOURCE_UNAVAILABLE,
                err.to_string(),
                &signer,
                &receipt_version,
            );
            store.lock().await.insert(receipt_id, updated);
            return;
        }
    };

    let decision = policy_engine.evaluate(request.venue, request.claim_type, &bundle);
    if !decision.ok {
        let updated = mark_non_provable(
            receipt,
            decision.reason.unwrap_or(NonProvableReason::POLICY_VIOLATION),
            decision.details,
            &signer,
            &receipt_version,
        );
        store.lock().await.insert(receipt_id, updated);
        return;
    }

    let statement = match adapter.build_statement(&request, &ack, &bundle).await {
        Ok(v) => v,
        Err(err) => {
            let updated = mark_non_provable(
                receipt,
                NonProvableReason::POLICY_VIOLATION,
                err.to_string(),
                &signer,
                &receipt_version,
            );
            store.lock().await.insert(receipt_id, updated);
            return;
        }
    };

    let claim_hash = hash_json(&serde_json::json!({
        "claim_type": request.claim_type,
        "statement": statement,
        "order_ref": request.order_ref,
        "execution_ref": request.execution_ref
    }));
    let venue_str = match request.venue {
        Venue::Hyperliquid => "hyperliquid",
        Venue::Base => "base",
        Venue::Solana => "solana",
        Venue::Polymarket => "polymarket",
    };
    let claim_type_str = match request.claim_type {
        ClaimType::ORDER_PLACED => "ORDER_PLACED",
        ClaimType::TRADE_EXECUTED => "TRADE_EXECUTED",
    };
    let public_inputs = serde_json::json!({
        "claim_hash": claim_hash,
        "evidence_root": bundle.evidence_root(),
        "venue": venue_str,
        "claim_type": claim_type_str
    });

    let proof = match prover.prove(&public_inputs).await {
        Ok(v) => v,
        Err(err) => {
            let updated = mark_non_provable(
                receipt,
                NonProvableReason::PROOF_FAILURE,
                err.to_string(),
                &signer,
                &receipt_version,
            );
            store.lock().await.insert(receipt_id, updated);
            return;
        }
    };

    let proved = build_proved_receipt(receipt, claim_hash, statement, bundle, proof, &signer, &receipt_version);
    let verified = verifier.verify(&proved).await;
    let final_receipt = if verified {
        proved
    } else {
        mark_non_provable(
            proved,
            NonProvableReason::PROOF_FAILURE,
            "Offchain verification failed for produced proof metadata.".to_string(),
            &signer,
            &receipt_version,
        )
    };
    store.lock().await.insert(receipt_id, final_receipt);
}

fn build_proved_receipt(
    mut receipt: ZKReceipt,
    claim_hash: String,
    statement: String,
    bundle: crate::models::EvidenceBundle,
    proof: ProofMetadata,
    signer: &str,
    receipt_version: &str,
) -> ZKReceipt {
    receipt.status = ReceiptStatus::PROVED;
    receipt.claim.statement = statement;
    receipt.claim.claim_hash = claim_hash.clone();
    receipt.provenance = Provenance {
        evidence_root: bundle.evidence_root(),
        evidence_items: bundle.items,
    };
    let now = now_iso();
    receipt.timing.updated_at = now.clone();
    receipt.timing.execution_observed_at = Some(now);
    receipt.timing.finality_observed_at = bundle.finality_observed_at;
    receipt.proof = proof.clone();
    receipt.integrity = build_integrity(
        signer,
        receipt_version,
        ReceiptStatus::PROVED,
        &claim_hash,
        &receipt.provenance.evidence_root,
        &proof.public_inputs_hash,
    );
    receipt.non_provable = None;
    receipt
}

fn mark_non_provable(
    mut receipt: ZKReceipt,
    reason: NonProvableReason,
    details: String,
    signer: &str,
    receipt_version: &str,
) -> ZKReceipt {
    let proof = no_proof_metadata();
    receipt.status = ReceiptStatus::NON_PROVABLE;
    receipt.non_provable = Some(NonProvable { reason_code: reason, details });
    receipt.timing.updated_at = now_iso();
    receipt.proof = proof.clone();
    receipt.integrity = build_integrity(
        signer,
        receipt_version,
        ReceiptStatus::NON_PROVABLE,
        &receipt.claim.claim_hash,
        &receipt.provenance.evidence_root,
        &proof.public_inputs_hash,
    );
    receipt
}

fn build_integrity(
    signer: &str,
    receipt_version: &str,
    status: ReceiptStatus,
    claim_hash: &str,
    evidence_root: &str,
    proof_hash: &str,
) -> Integrity {
    let schema_hash = hash_json(&serde_json::json!({
        "schema": "zkreceipt.schema.json",
        "version": receipt_version
    }));
    let receipt_hash = hash_json(&serde_json::json!({
        "status": status,
        "claim_hash": claim_hash,
        "evidence_root": evidence_root,
        "proof_hash": proof_hash
    }));
    let signature = hash_json(&serde_json::json!({
        "signer": signer,
        "receipt_hash": receipt_hash
    }));
    Integrity {
        schema_hash,
        receipt_hash,
        signer: signer.to_string(),
        signature,
    }
}
