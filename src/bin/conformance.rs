use anyhow::{bail, Context, Result};
use serde_json::Value;
use sha2::{Digest, Sha256};
use std::collections::{HashMap, HashSet};
use std::fs;
use std::path::{Path, PathBuf};

fn main() -> Result<()> {
    let root = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    let spec_dir = root.join("spec");
    let bench_dir = root.join("benchmarks");

    let claim_taxonomy = read_json(&spec_dir.join("claim-taxonomy.json"))?;
    let source_precedence = read_json(&spec_dir.join("source-precedence.json"))?;
    let pipeline_lifecycle = read_json(&spec_dir.join("pipeline-lifecycle.json"))?;
    let slos = read_json(&bench_dir.join("phase0_slos.json"))?;
    let workloads = read_json(&bench_dir.join("workloads.json"))?;

    validate_claim_taxonomy(&claim_taxonomy)?;
    validate_source_precedence(&source_precedence)?;
    if pipeline_lifecycle.get("states").is_none() {
        bail!("pipeline-lifecycle: missing states");
    }
    if slos.get("objectives").is_none() {
        bail!("phase0_slos: missing objectives");
    }

    let digests = validate_workloads_and_digests(&workloads, &claim_taxonomy)?;

    println!("Phase 0 conformance checks passed.");
    println!("Deterministic scenario digests:");
    for (id, digest) in digests {
        println!("  - {}: {}", id, digest);
    }
    Ok(())
}

fn read_json(path: &Path) -> Result<Value> {
    let content = fs::read_to_string(path).with_context(|| format!("failed to read {}", path.display()))?;
    let parsed: Value =
        serde_json::from_str(&content).with_context(|| format!("failed to parse {}", path.display()))?;
    Ok(parsed)
}

fn validate_claim_taxonomy(data: &Value) -> Result<()> {
    let claim_types = data
        .get("claim_types")
        .and_then(|v| v.as_object())
        .ok_or_else(|| anyhow::anyhow!("claim-taxonomy: missing claim_types"))?;

    for required in ["ORDER_PLACED", "TRADE_EXECUTED"] {
        if !claim_types.contains_key(required) {
            bail!("claim-taxonomy: missing claim type {}", required);
        }
    }

    let reason_codes: HashSet<String> = data
        .get("non_provable_reason_codes")
        .and_then(|v| v.as_array())
        .ok_or_else(|| anyhow::anyhow!("claim-taxonomy: missing non_provable_reason_codes"))?
        .iter()
        .filter_map(|v| v.as_str().map(str::to_string))
        .collect();

    let required_reason_codes: HashSet<String> = [
        "EVIDENCE_MISSING",
        "EVIDENCE_CONFLICT",
        "SOURCE_UNAVAILABLE",
        "FINALITY_TIMEOUT",
        "POLICY_VIOLATION",
        "SCHEMA_INVALID",
        "UNSUPPORTED_VENUE_CLAIM",
        "PROOF_FAILURE",
    ]
    .iter()
    .map(|s| (*s).to_string())
    .collect();

    if !required_reason_codes.is_subset(&reason_codes) {
        bail!("claim-taxonomy: missing required non_provable_reason_codes");
    }
    Ok(())
}

fn validate_source_precedence(data: &Value) -> Result<()> {
    let venues = data
        .get("venues")
        .and_then(|v| v.as_object())
        .ok_or_else(|| anyhow::anyhow!("source-precedence: missing venues"))?;

    for venue in ["hyperliquid", "base", "solana", "polymarket"] {
        let cfg = venues
            .get(venue)
            .and_then(|v| v.as_object())
            .ok_or_else(|| anyhow::anyhow!("source-precedence: missing venue policy {}", venue))?;
        if !cfg.contains_key("order_placed_sources_preferred")
            || !cfg.contains_key("trade_executed_sources_preferred")
        {
            bail!("source-precedence: missing source preference lists for {}", venue);
        }
    }
    Ok(())
}

fn validate_workloads_and_digests(workloads: &Value, taxonomy: &Value) -> Result<Vec<(String, String)>> {
    let scenarios = workloads
        .get("scenarios")
        .and_then(|v| v.as_array())
        .ok_or_else(|| anyhow::anyhow!("workloads: scenarios must be non-empty"))?;
    if scenarios.is_empty() {
        bail!("workloads: scenarios must be non-empty");
    }

    let required_tags_by_claim: HashMap<String, HashSet<String>> = taxonomy
        .get("claim_types")
        .and_then(|v| v.as_object())
        .ok_or_else(|| anyhow::anyhow!("claim-taxonomy: missing claim_types"))?
        .iter()
        .map(|(claim, cfg)| {
            let tags: HashSet<String> = cfg
                .get("required_evidence_tags_all")
                .and_then(|v| v.as_array())
                .into_iter()
                .flatten()
                .filter_map(|v| v.as_str().map(str::to_string))
                .collect();
            (claim.clone(), tags)
        })
        .collect();

    let allowed_venues: HashSet<&str> = ["hyperliquid", "base", "solana", "polymarket"].into_iter().collect();
    let allowed_claims: HashSet<&str> = ["ORDER_PLACED", "TRADE_EXECUTED"].into_iter().collect();

    let mut seen_ids = HashSet::new();
    let mut digests = Vec::with_capacity(scenarios.len());

    for scenario in scenarios {
        let id = scenario
            .get("id")
            .and_then(|v| v.as_str())
            .ok_or_else(|| anyhow::anyhow!("workloads: scenario missing id"))?
            .to_string();
        if !seen_ids.insert(id.clone()) {
            bail!("workloads: duplicate scenario id {}", id);
        }

        let venue = scenario
            .get("venue")
            .and_then(|v| v.as_str())
            .ok_or_else(|| anyhow::anyhow!("workloads: scenario {} missing venue", id))?;
        if !allowed_venues.contains(venue) {
            bail!("workloads: unsupported venue {}", venue);
        }

        let claim_type = scenario
            .get("claim_type")
            .and_then(|v| v.as_str())
            .ok_or_else(|| anyhow::anyhow!("workloads: scenario {} missing claim_type", id))?;
        if !allowed_claims.contains(claim_type) {
            bail!("workloads: unsupported claim {}", claim_type);
        }

        let evidence_profile: HashSet<String> = scenario
            .get("evidence_profile")
            .and_then(|v| v.as_array())
            .ok_or_else(|| anyhow::anyhow!("workloads: scenario {} missing evidence_profile", id))?
            .iter()
            .filter_map(|v| v.as_str().map(str::to_string))
            .collect();

        let required_tags = required_tags_by_claim
            .get(claim_type)
            .ok_or_else(|| anyhow::anyhow!("workloads: unknown claim type {}", claim_type))?;
        if !required_tags.is_subset(&evidence_profile) {
            bail!(
                "workloads: scenario {} missing required evidence tags for {}",
                id,
                claim_type
            );
        }

        let mut sorted_profile: Vec<String> = evidence_profile.iter().cloned().collect();
        sorted_profile.sort();
        let digest_input = serde_json::json!({
            "venue": venue,
            "claim_type": claim_type,
            "action_template": scenario.get("action_template").and_then(|v| v.as_str()).unwrap_or(""),
            "evidence_profile": sorted_profile,
            "payload_bytes_target": scenario.get("payload_bytes_target").and_then(|v| v.as_u64()).unwrap_or(0)
        });
        let digest = sha256_json(&digest_input)?;
        digests.push((id, digest));
    }
    Ok(digests)
}

fn sha256_json(value: &Value) -> Result<String> {
    let bytes = serde_json::to_vec(value)?;
    let mut hasher = Sha256::new();
    hasher.update(bytes);
    Ok(hex::encode(hasher.finalize()))
}
