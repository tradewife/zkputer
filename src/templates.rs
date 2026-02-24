use crate::models::{ClaimType, ProofRequest, Venue};
use anyhow::{anyhow, Result};
use serde::Serialize;
use serde_json::{Map, Value};

pub const TEMPLATE_ORDER_PLACEMENT_VERIFICATION: &str = "order_placement_verification";
pub const TEMPLATE_TRADE_EXECUTION_VERIFICATION: &str = "trade_execution_verification";

#[derive(Debug, Clone, Serialize)]
pub struct VerificationTemplate {
    pub template_id: &'static str,
    pub name: &'static str,
    pub claim_type: ClaimType,
    pub description: &'static str,
    pub required_fields: &'static [&'static str],
    pub optional_fields: &'static [&'static str],
}

pub fn list_verification_templates() -> Vec<VerificationTemplate> {
    vec![
        VerificationTemplate {
            template_id: TEMPLATE_ORDER_PLACEMENT_VERIFICATION,
            name: "Order placement verification",
            claim_type: ClaimType::ORDER_PLACED,
            description:
                "Verifies that an order placement action was accepted by the target venue.",
            required_fields: &["venue", "account_ref", "order_ref"],
            optional_fields: &["wait_for_result", "wait_timeout_ms", "client_order_id", "notes"],
        },
        VerificationTemplate {
            template_id: TEMPLATE_TRADE_EXECUTION_VERIFICATION,
            name: "Trade execution verification",
            claim_type: ClaimType::TRADE_EXECUTED,
            description:
                "Verifies that a trade execution artifact exists for an order on the target venue.",
            required_fields: &["venue", "account_ref", "order_ref", "execution_ref"],
            optional_fields: &["wait_for_result", "wait_timeout_ms", "fill_qty", "fill_price", "notes"],
        },
    ]
}

pub fn template_ids() -> Vec<&'static str> {
    list_verification_templates()
        .into_iter()
        .map(|t| t.template_id)
        .collect()
}

pub fn build_request_from_template(template_id: &str, template_args: &Value) -> Result<ProofRequest> {
    let args = template_args
        .as_object()
        .ok_or_else(|| anyhow!("template_args must be an object"))?;

    let venue = parse_venue(required_string(args, "venue")?.as_str())?;
    let account_ref = required_string(args, "account_ref")?;
    let order_ref = required_string(args, "order_ref")?;
    let execution_ref = optional_string(args, "execution_ref");

    let (claim_type, required_execution_ref) = match template_id {
        TEMPLATE_ORDER_PLACEMENT_VERIFICATION => (ClaimType::ORDER_PLACED, false),
        TEMPLATE_TRADE_EXECUTION_VERIFICATION => (ClaimType::TRADE_EXECUTED, true),
        _ => return Err(anyhow!("unsupported template_id: {}", template_id)),
    };

    if required_execution_ref && execution_ref.is_none() {
        return Err(anyhow!(
            "template {} requires execution_ref",
            TEMPLATE_TRADE_EXECUTION_VERIFICATION
        ));
    }

    let mut payload_map = args.clone();
    for key in [
        "venue",
        "account_ref",
        "order_ref",
        "execution_ref",
        "wait_for_result",
        "wait_timeout_ms",
    ] {
        payload_map.remove(key);
    }
    payload_map.insert(
        "template".to_string(),
        serde_json::json!({
            "template_id": template_id,
            "template_version": "v1"
        }),
    );

    Ok(ProofRequest {
        venue,
        claim_type,
        account_ref,
        order_ref,
        execution_ref,
        payload: Value::Object(payload_map),
    })
}

fn parse_venue(raw: &str) -> Result<Venue> {
    match raw {
        "hyperliquid" => Ok(Venue::Hyperliquid),
        "base" => Ok(Venue::Base),
        "solana" => Ok(Venue::Solana),
        "polymarket" => Ok(Venue::Polymarket),
        _ => Err(anyhow!("unsupported venue: {}", raw)),
    }
}

fn required_string(args: &Map<String, Value>, field: &str) -> Result<String> {
    args.get(field)
        .and_then(|v| v.as_str())
        .map(|s| s.to_string())
        .ok_or_else(|| anyhow!("{} is required", field))
}

fn optional_string(args: &Map<String, Value>, field: &str) -> Option<String> {
    args.get(field)
        .and_then(|v| v.as_str())
        .map(|s| s.to_string())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn builds_order_placement_request() {
        let req = build_request_from_template(
            TEMPLATE_ORDER_PLACEMENT_VERIFICATION,
            &serde_json::json!({
                "venue": "base",
                "account_ref": "acct-1",
                "order_ref": "order-1",
                "notes": "smoke"
            }),
        )
        .expect("template should build");
        assert_eq!(req.claim_type, ClaimType::ORDER_PLACED);
        assert_eq!(req.execution_ref, None);
        assert_eq!(req.payload["notes"], "smoke");
        assert_eq!(req.payload["template"]["template_id"], TEMPLATE_ORDER_PLACEMENT_VERIFICATION);
    }

    #[test]
    fn execution_template_requires_execution_ref() {
        let result = build_request_from_template(
            TEMPLATE_TRADE_EXECUTION_VERIFICATION,
            &serde_json::json!({
                "venue": "solana",
                "account_ref": "acct-2",
                "order_ref": "order-2"
            }),
        );
        assert!(result.is_err());
    }
}
