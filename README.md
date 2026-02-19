# zkputer
zkputer is a universal verification layer for agent actions.

It gives agents a simple tool-call to request cryptographic receipts for what happened on external venues, without changing their execution stack.

## One-line pitch
Agents execute. zkputer verifies.

## Grant/Deck brief
### Problem
Agent execution is scaling faster than verification infrastructure. In many workflows, it is still hard to independently verify whether claimed actions (such as order placement or execution) actually happened under explicit policy.

### Solution
zkputer adds a cryptographic verification layer as a tool-call. It converts venue evidence into machine-verifiable receipts for binary claims (`ORDER_PLACED`, `TRADE_EXECUTED`) and returns `NON_PROVABLE` when truth cannot be established safely.

### Why now
- Agent adoption is accelerating across trading and automation.
- ZK systems are now practical enough for production verification paths.
- There is no dominant universal middleware focused on agent action receipts across these target venues.

### Outcome
zkputer makes automation more trustworthy by making verification portable, explicit, and independently checkable.

## What this project is
- A verification middleware for agent workflows.
- A receipt system for binary trade claims.
- A trust layer designed for speed, transparency, and independent verification.

## What this project is not
- Not a trading bot.
- Not an execution router.
- Not a custody layer.
- Not a guarantee engine for strategy quality, PnL, or “best execution.”

zkputer does not place orders. It verifies evidence about orders and executions produced by existing agent tools.

## Why it matters
Agent systems are scaling faster than trust infrastructure.

When agents interact with markets, users and downstream systems need cryptographic receipts that answer:
- Was an order actually placed?
- Was a trade actually executed?
- What evidence was used?
- Under what policy and finality assumptions was this judged?

zkputer is built to provide those answers in a machine-verifiable format.

## Who this is for
- Agent framework builders that need verification primitives
- Trading agent operators that need auditable receipts
- Integrators that need machine-checkable execution evidence
- Security/compliance teams that need explicit assumptions and replayable artifacts

## Core claims
zkputer currently supports two binary claim types:
- `ORDER_PLACED`
- `TRADE_EXECUTED`

If required evidence is missing, conflicting, stale, or policy-invalid, zkputer returns `NON_PROVABLE` (fail-closed).

## Launch venues
V1 target venues:
- Hyperliquid
- Base
- Solana
- Polymarket

## Product principles
- Verification-only boundary (no trade execution)
- Non-blocking proof pipeline
- Fail-closed truth handling
- Explicit trust assumptions and policy versioning
- Venue-agnostic receipt semantics

## How the flow works
1. Agent executes through its existing venue integration.
2. Agent (or orchestrator) calls zkputer verification.
3. zkputer gathers and normalizes provenance-tagged evidence.
4. zkputer evaluates policy and finality rules.
5. zkputer emits a receipt with status: `PENDING`, `PROVED`, `NON_PROVABLE`, or `INVALIDATED`.

This is intentionally asynchronous and non-blocking so proof generation does not slow order flow.

## Trust model
Working phrase:
Zero-trust compute verification with trust-scoped data provenance.

Meaning:
- ZK verification can provide near-zero-trust guarantees about computation integrity.
- Real-world truth still depends on evidence provenance, source authenticity, and finality context.

Canonical trust docs:
- `spec/trust-model.txt`
- `spec/source-precedence.json`
- `spec/claim-taxonomy.json`
- `spec/zkreceipt.schema.json`

## Verification strategy
- Default: offchain-first verification for speed.
- Optional: batched onchain anchoring for public auditability and composability.

## MVP runtime profile (lean prototype)
- Proving backend for MVP: SP1 only.
- Proving infrastructure: Boundless cloud.
- No independent RPC cross-checking in MVP path (kept in roadmap for trust hardening).
- Pico fallback is roadmap, not in MVP runtime.

## Monetization direction
- Metered verification tool-call usage
- Optional premium lane for privacy-enhanced verification
- Potential enterprise tier for policy controls, audit surfaces, and reliability SLOs

## Privacy strategy
Privacy is optional at launch.
- Fast lane: standard verification.
- Private lane: opt-in privacy path with explicit latency/cost tradeoffs.

## Security posture
- Fail-closed on ambiguity (`NON_PROVABLE`).
- Explicit policy versioning and source precedence.
- Evidence-rooted receipts with reproducible verification context.
- Transparent assumptions attached to each receipt.

## Current repository status
This repo currently contains:
- Canonical specs and conformance artifacts.
- Benchmark targets and workload definitions.
- Rust runtime scaffolding for receipt lifecycle, policy checks, and verification flow.
Until live venue/prover integrations are wired, synthetic Rust adapters are placeholders for interface and behavior development.
Until live venue/prover integrations are wired, synthetic components are placeholders for interface and behavior development.

## Repo map
- `spec/` canonical specs (claims, trust model, lifecycle, schema, source precedence)
- `benchmarks/` SLO targets and benchmark workloads
- `src/` Rust runtime engine, adapters, prover, verifier, and demo/conformance binaries
- `tests/` Rust behavioral tests

## Local checks
- `cargo test`
- `cargo run --bin demo`
- `cargo run --bin conformance`

## Near-term build path
1. Replace synthetic adapters with live venue adapters.
2. Wire production proving backends and verifier flows.
3. Enforce per-venue precedence + finality policies in production paths.
4. Expose OpenClaw-oriented verification tool-call surface.

## Current asks for partners
- Early design partners for production traffic and feedback loops
- Security reviewers for trust/policy assumptions and failure handling
- Integration partners across agent frameworks and venue adapters

## Product language guardrail
Use “cryptographically verifiable under declared assumptions.”
Avoid absolute legal guarantees while provenance, policy, and finality assumptions remain context-dependent.

## Universal agent access (MVP)
Primary integration surface is MCP.

- Start server: `cargo run --bin mcp_server`
- Exposed tools:
  - `zkputer_verify_claim`
  - `zkputer_get_receipt`

Provided integration examples:
- Warp: `integrations/warp/mcp.json`
- Claude Code: `integrations/claude/.mcp.json`
- Codex: `integrations/codex/config.toml`
- OpenClaw plugin skeleton: `integrations/openclaw-plugin/`

Notes:
- OpenClaw integration is plugin-first for tool registration.
- Skills can be layered later for behavior guidance, but MCP/tool surfaces are the execution interface.
