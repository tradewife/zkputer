# zkputer verification skill (MVP)
Use this skill when an agent needs cryptographic verification receipts for onchain or venue actions.

## Goal
Treat zkputer as the seamless link between agent execution and zk proof generation.
Do not call Succinct/SP1 APIs directly from agent workflows in MVP paths.

## Preferred tool sequence
1. Call `zkputer_list_templates` to discover supported hardened templates.
2. Choose the narrowest template for the claim.
3. Call `zkputer_verify_template` with `template_id` and `template_args`.
4. If `wait_for_result` is false (or timeout is reached), poll with `zkputer_get_receipt`.
5. Continue workflow only when receipt status is acceptable for policy (`PROVED` or explicitly handled `NON_PROVABLE`).

## Hardened templates (MVP)
- `order_placement_verification`
  - Required args: `venue`, `account_ref`, `order_ref`
- `trade_execution_verification`
  - Required args: `venue`, `account_ref`, `order_ref`, `execution_ref`

## Receipt handling policy
- `PROVED`: Verification succeeded.
- `NON_PROVABLE`: Fail closed; do not infer success.
- `PENDING`: Retry/poll.
- `INVALIDATED`: Treat as not valid; escalate.

## Example call shapes
### Verify order placement
`zkputer_verify_template`
```json
{
  "template_id": "order_placement_verification",
  "template_args": {
    "venue": "base",
    "account_ref": "acct-123",
    "order_ref": "ord-456"
  },
  "wait_for_result": true,
  "wait_timeout_ms": 5000
}
```

### Verify trade execution
`zkputer_verify_template`
```json
{
  "template_id": "trade_execution_verification",
  "template_args": {
    "venue": "hyperliquid",
    "account_ref": "acct-123",
    "order_ref": "ord-456",
    "execution_ref": "exec-789"
  },
  "wait_for_result": true,
  "wait_timeout_ms": 8000
}
```

## Adaptation guidance
- Prefer template extension through zkputer template registry updates instead of ad-hoc agent-side proof logic.
- Keep venue-specific nuance in `template_args` metadata fields, not in direct prover calls.
