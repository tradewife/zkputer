# OpenClaw plugin integration (MVP)
This plugin registers `zkputer_verify_claim` and `zkputer_get_receipt` tools and proxies tool calls to the Rust MCP server over stdio.

## Install locally
Install from this directory using your OpenClaw-compatible plugin install command.

## Default behavior
If no config is provided, the plugin starts:
- command: `cargo`
- args: `run --manifest-path <cwd>/Cargo.toml --bin mcp_server`

For reliability, set explicit config in your plugin settings.

## Recommended config
```json
{
  "mcpServerCommand": "cargo",
  "mcpServerArgs": [
    "run",
    "--manifest-path",
    "/home/kt/zkputer/Cargo.toml",
    "--bin",
    "mcp_server"
  ],
  "requestTimeoutMs": 15000
}
```

## Tool contract
- `zkputer_verify_claim`
  - required: `venue`, `claim_type`, `account_ref`, `order_ref`
  - optional: `execution_ref`, `wait_for_result`, `wait_timeout_ms`
- `zkputer_get_receipt`
  - required: `receipt_id`
