use anyhow::{anyhow, Context, Result};
use serde::{Deserialize, Serialize};
use serde_json::{json, Value};
use std::io::{self, BufRead, BufReader, Write};
use std::sync::Arc;
use std::time::Duration;
use tokio::runtime::Runtime;
use zkputer::adapters::{SyntheticVenueAdapter, VenueAdapter};
use zkputer::models::{ClaimType, ProofRequest, Venue};
use zkputer::policy::PolicyEngine;
use zkputer::verifier::OffchainVerifier;
use zkputer::{ReceiptEngine, Sp1MvpProver};

#[derive(Debug, Deserialize)]
struct JsonRpcRequest {
    #[allow(dead_code)]
    jsonrpc: Option<String>,
    id: Option<Value>,
    method: String,
    params: Option<Value>,
}

#[derive(Debug, Serialize)]
struct JsonRpcResponse {
    jsonrpc: &'static str,
    id: Value,
    #[serde(skip_serializing_if = "Option::is_none")]
    result: Option<Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    error: Option<Value>,
}

fn main() -> Result<()> {
    let runtime = Runtime::new().context("failed to create tokio runtime")?;
    let engine = runtime.block_on(build_engine())?;

    let stdin = io::stdin();
    let stdout = io::stdout();
    let mut reader = BufReader::new(stdin.lock());
    let mut writer = stdout.lock();

    while let Some(message) = read_message(&mut reader)? {
        let request: JsonRpcRequest = match serde_json::from_slice(&message) {
            Ok(v) => v,
            Err(err) => {
                let response = JsonRpcResponse {
                    jsonrpc: "2.0",
                    id: Value::Null,
                    result: None,
                    error: Some(json!({"code": -32700, "message": format!("Parse error: {}", err)})),
                };
                write_message(&mut writer, &response)?;
                continue;
            }
        };

        if let Some(id) = request.id.clone() {
            let response = handle_request(&runtime, &engine, request, id);
            write_message(&mut writer, &response)?;
        } else if request.method == "notifications/initialized" {
            continue;
        }
    }

    Ok(())
}

async fn build_engine() -> Result<ReceiptEngine> {
    let adapters: Vec<Arc<dyn VenueAdapter>> = vec![
        Arc::new(SyntheticVenueAdapter::new(Venue::Hyperliquid)),
        Arc::new(SyntheticVenueAdapter::new(Venue::Base)),
        Arc::new(SyntheticVenueAdapter::new(Venue::Solana)),
        Arc::new(SyntheticVenueAdapter::new(Venue::Polymarket)),
    ];
    let engine = ReceiptEngine::new(
        adapters,
        PolicyEngine::new(None)?,
        Arc::new(Sp1MvpProver),
        OffchainVerifier::default(),
    );
    Ok(engine)
}

fn handle_request(runtime: &Runtime, engine: &ReceiptEngine, request: JsonRpcRequest, id: Value) -> JsonRpcResponse {
    let method = request.method.as_str();
    let params = request.params.unwrap_or_else(|| json!({}));
    let result = match method {
        "initialize" => Ok(json!({
            "protocolVersion": "2024-11-05",
            "capabilities": { "tools": {} },
            "serverInfo": {
                "name": "zkputer-mcp",
                "version": "0.1.0"
            }
        })),
        "ping" => Ok(json!({})),
        "tools/list" => Ok(json!({
            "tools": [
                {
                    "name": "zkputer_verify_claim",
                    "description": "Submit a verification request and optionally wait for a receipt.",
                    "inputSchema": {
                        "type": "object",
                        "additionalProperties": false,
                        "properties": {
                            "venue": { "type": "string", "enum": ["hyperliquid","base","solana","polymarket"] },
                            "claim_type": { "type": "string", "enum": ["ORDER_PLACED","TRADE_EXECUTED"] },
                            "account_ref": { "type": "string" },
                            "order_ref": { "type": "string" },
                            "execution_ref": { "type": "string" },
                            "wait_for_result": { "type": "boolean", "default": true },
                            "wait_timeout_ms": { "type": "integer", "default": 3000 }
                        },
                        "required": ["venue","claim_type","account_ref","order_ref"]
                    }
                },
                {
                    "name": "zkputer_get_receipt",
                    "description": "Fetch a previously created receipt by id.",
                    "inputSchema": {
                        "type": "object",
                        "additionalProperties": false,
                        "properties": {
                            "receipt_id": { "type": "string" }
                        },
                        "required": ["receipt_id"]
                    }
                }
            ]
        })),
        "tools/call" => handle_tool_call(runtime, engine, &params),
        _ => Err(anyhow!("Method not found: {}", method)),
    };

    match result {
        Ok(result) => JsonRpcResponse {
            jsonrpc: "2.0",
            id,
            result: Some(result),
            error: None,
        },
        Err(err) => {
            let code = if method == "tools/call" { -32000 } else { -32601 };
            JsonRpcResponse {
                jsonrpc: "2.0",
                id,
                result: None,
                error: Some(json!({
                    "code": code,
                    "message": err.to_string()
                })),
            }
        }
    }
}

fn handle_tool_call(runtime: &Runtime, engine: &ReceiptEngine, params: &Value) -> Result<Value> {
    let name = params
        .get("name")
        .and_then(|v| v.as_str())
        .ok_or_else(|| anyhow!("tools/call missing name"))?;
    let arguments = params.get("arguments").cloned().unwrap_or_else(|| json!({}));

    match name {
        "zkputer_verify_claim" => {
            let venue = parse_venue(arguments.get("venue").and_then(|v| v.as_str()))
                .ok_or_else(|| anyhow!("invalid venue"))?;
            let claim_type = parse_claim_type(arguments.get("claim_type").and_then(|v| v.as_str()))
                .ok_or_else(|| anyhow!("invalid claim_type"))?;
            let account_ref = arguments
                .get("account_ref")
                .and_then(|v| v.as_str())
                .ok_or_else(|| anyhow!("account_ref is required"))?
                .to_string();
            let order_ref = arguments
                .get("order_ref")
                .and_then(|v| v.as_str())
                .ok_or_else(|| anyhow!("order_ref is required"))?
                .to_string();
            let execution_ref = arguments
                .get("execution_ref")
                .and_then(|v| v.as_str())
                .map(|s| s.to_string());
            let wait_for_result = arguments
                .get("wait_for_result")
                .and_then(|v| v.as_bool())
                .unwrap_or(true);
            let wait_timeout_ms = arguments
                .get("wait_timeout_ms")
                .and_then(|v| v.as_u64())
                .unwrap_or(3000);

            let request = ProofRequest {
                venue,
                claim_type,
                account_ref,
                order_ref,
                execution_ref,
                payload: json!({}),
            };
            let receipt_id = runtime.block_on(engine.submit(request))?;
            let receipt = if wait_for_result {
                runtime.block_on(engine.wait_for_receipt(
                    &receipt_id,
                    Duration::from_millis(wait_timeout_ms),
                ))?
            } else {
                runtime
                    .block_on(engine.get_receipt(&receipt_id))
                    .ok_or_else(|| anyhow!("receipt not found after submit"))?
            };
            let payload = serde_json::to_value(&receipt)?;
            Ok(json!({
                "content": [{
                    "type": "text",
                    "text": serde_json::to_string_pretty(&payload)?
                }],
                "structuredContent": payload
            }))
        }
        "zkputer_get_receipt" => {
            let receipt_id = arguments
                .get("receipt_id")
                .and_then(|v| v.as_str())
                .ok_or_else(|| anyhow!("receipt_id is required"))?;
            let maybe_receipt = runtime.block_on(engine.get_receipt(receipt_id));
            match maybe_receipt {
                Some(receipt) => {
                    let payload = serde_json::to_value(&receipt)?;
                    Ok(json!({
                        "content": [{
                            "type": "text",
                            "text": serde_json::to_string_pretty(&payload)?
                        }],
                        "structuredContent": payload
                    }))
                }
                None => Ok(json!({
                    "isError": true,
                    "content": [{
                        "type": "text",
                        "text": format!("receipt not found: {}", receipt_id)
                    }]
                })),
            }
        }
        _ => Ok(json!({
            "isError": true,
            "content": [{
                "type": "text",
                "text": format!("unknown tool: {}", name)
            }]
        })),
    }
}

fn parse_venue(value: Option<&str>) -> Option<Venue> {
    match value? {
        "hyperliquid" => Some(Venue::Hyperliquid),
        "base" => Some(Venue::Base),
        "solana" => Some(Venue::Solana),
        "polymarket" => Some(Venue::Polymarket),
        _ => None,
    }
}

fn parse_claim_type(value: Option<&str>) -> Option<ClaimType> {
    match value? {
        "ORDER_PLACED" => Some(ClaimType::ORDER_PLACED),
        "TRADE_EXECUTED" => Some(ClaimType::TRADE_EXECUTED),
        _ => None,
    }
}

fn read_message<R: BufRead>(reader: &mut R) -> Result<Option<Vec<u8>>> {
    let mut content_length: Option<usize> = None;
    loop {
        let mut line = String::new();
        let bytes = reader.read_line(&mut line)?;
        if bytes == 0 {
            return Ok(None);
        }
        let trimmed = line.trim_end_matches(['\r', '\n']);
        if trimmed.is_empty() {
            break;
        }
        if let Some(v) = trimmed.strip_prefix("Content-Length:") {
            content_length = Some(v.trim().parse::<usize>().context("invalid Content-Length")?);
        }
    }

    let length = content_length.ok_or_else(|| anyhow!("missing Content-Length header"))?;
    let mut body = vec![0u8; length];
    std::io::Read::read_exact(reader, &mut body)?;
    Ok(Some(body))
}

fn write_message<W: Write>(writer: &mut W, payload: &impl Serialize) -> Result<()> {
    let body = serde_json::to_vec(payload)?;
    write!(writer, "Content-Length: {}\r\n\r\n", body.len())?;
    writer.write_all(&body)?;
    writer.flush()?;
    Ok(())
}
