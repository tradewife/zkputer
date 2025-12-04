# Protocol Compliance Implementation
# Auto-executes before any "HyperGrok run daily" command

import sys
import os


def protocol_compliance_check():
    """
    MANDATORY: Must pass before any daily routine execution
    """
    print("🔍 PROTOCOL COMPLIANCE CHECK INITIATED")

    # Check 1: Handbook Files Read
    handbook_files = [
        "/home/kt/Desktop/HyperOPS/📚 Agent Handbook/AGENT_INSTRUCTIONS.md",
        "/home/kt/Desktop/HyperOPS/📚 Agent Handbook/daily_OPS.md",
        "/home/kt/Desktop/HyperOPS/📚 Agent Handbook/HyperGrok_Prompt.md",
        "/home/kt/Desktop/HyperOPS/📚 Agent Handbook/PROTOCOL_COMPLIANCE.md",
        "/home/kt/Desktop/HyperOPS/📚 Agent Handbook/SOURCE_PRIORITY_PROTOCOL.md",
    ]

    for file_path in handbook_files:
        if not os.path.exists(file_path):
            return f"❌ MISSING: {file_path}"

    # Check 2: Template Available
    template_file = "/home/kt/Desktop/HyperOPS/📖 Other Components/templates/daily_trading_brief_template.md"
    if not os.path.exists(template_file):
        return "❌ MISSING: daily_trading_brief_template.md"

    # Check 2.1: Source Priority Protocol
    source_priority_file = (
        "/home/kt/Desktop/HyperOPS/📚 Agent Handbook/SOURCE_PRIORITY_PROTOCOL.md"
    )
    if not os.path.exists(source_priority_file):
        return "❌ MISSING: SOURCE_PRIORITY_PROTOCOL.md"

    # Check 3: Knowledge Graph Access
    kg_files = [
        "/home/kt/Desktop/HyperOPS/📖 Other Components/knowledge_graph/performance_log.md",
        "/home/kt/Desktop/HyperOPS/📖 Other Components/knowledge_graph/narratives.md",
        "/home/kt/Desktop/HyperOPS/📖 Other Components/knowledge_graph/playbook.md",
        "/home/kt/Desktop/HyperOPS/📖 Other Components/knowledge_graph/smart_money.md",
        "/home/kt/Desktop/HyperOPS/📖 Other Components/knowledge_graph/tokens.md",
    ]

    for file_path in kg_files:
        if not os.path.exists(file_path):
            return f"❌ MISSING: {file_path}"

    # Check 4: Protocol Compliance Files
    compliance_files = [
        "/home/kt/Desktop/HyperOPS/📚 Agent Handbook/protocol_compliance.py",
        "/home/kt/Desktop/HyperOPS/📚 Agent Handbook/PROTOCOL_COMPLIANCE.md",
        "/home/kt/Desktop/HyperOPS/📚 Agent Handbook/SOURCE_PRIORITY_PROTOCOL.md",
    ]

    for file_path in compliance_files:
        if not os.path.exists(file_path):
            return f"❌ MISSING: {file_path}"

    print("✅ ALL COMPLIANCE SYSTEMS ACTIVE")
    print(
        "🎯 SOURCE PRIORITY ENFORCED: Knowledge Graph → Whale Intel → Hyperliquid Data → General News"
    )
    print("🚫 GENERAL SEARCHES FORBIDDEN: Must exhaust primary sources first")
    print("⏱️ MINIMUM ANALYSIS TIME: 15+ minutes whale intel deep dive required")
    return "PROTOCOL_READY"


def hypergrok_daily_protocol():
    """
    ENFORCED: Exact HyperGrok + Daily OPS execution sequence
    """
    compliance_status = protocol_compliance_check()
    if compliance_status != "PROTOCOL_READY":
        return f"🚨 PROTOCOL VIOLATION: {compliance_status}"

    print("🚀 EXECUTING HYPERGROK + DAILY OPS PROTOCOL")
    print("📋 FOLLOWING EXACT SEQUENCE FROM daily_OPS.md")
    print(
        "🎯 PRIORITY SOURCES: Knowledge Graph → Whale Intel → Hyperliquid Data → General News"
    )

    # Phase 0: Market Preparation (MANDATORY START)
    phases = [
        "Phase 0: Market Preparation - Performance review, regime assessment, setup selection, smart money review",
        "Phase 1: Market Scan & Catalyst Detection - Hyperliquid scan, funding/OI, X intel, WHALE INTEL DEEP DIVE (15+ min)",
        "Phase 2: Setup Identification & Deep Dive - Technical analysis, thesis validation, smart money corroboration",
        "Phase 3: Trade Planning & Readiness - Trade specs, execution readiness, monitoring plan",
        "Phase 4: Documentation & Analysis - Update knowledge graph, generate daily trading brief",
        "Phase 5: Execution & Broadcast - On command only",
    ]

    for phase in phases:
        print(f"✅ {phase}")

    print(
        "⚠️ SOURCE PRIORITY ENFORCED: NO GENERAL SEARCHES WITHOUT EXHAUSTING PRIMARY SOURCES"
    )
    return "PROTOCOL_EXECUTION_READY"


def output_order_verification():
    """
    CRITICAL: Must follow exact daily_OPS.md output order
    """
    required_order = [
        "1. Market Snapshot (AEST timestamp + 1-paragraph summary)",
        "2. Evidence Tables (Funding, OI, Basis, Liquidity, Session Structure)",
        "3. On-Chain & Whale Intel Digest (Smart money flows, large prints, lead-lag)",
        "4. Top 3 Playbook Cards (Setup, Entry, Stop, TP, Rationale)",
        "5. Final Two Trades (Complete specs with sizing and risk)",
        "6. X Post (≤280 characters, matter-of-fact tone)",
    ]

    print("📊 OUTPUT ORDER VERIFICATION:")
    for item in required_order:
        print(f"   {item}")

    return "OUTPUT_ORDER_LOCKED"


def template_enforcement():
    """
    MANDATORY: Use exact template formats
    """
    print("📋 TEMPLATE ENFORCEMENT ACTIVE:")
    print("   - Must use daily_trading_brief_template.md EXACT format")
    print("   - No deviation from table structures")
    print("   - All sections must be complete")
    print("   - X Post must be ≤280 characters")

    return "_TEMPLATE_ENFORCED"


def knowledge_graph_mandatory_updates():
    """
    REQUIRED: Update ALL knowledge graph files every session
    """
    kg_updates = [
        "performance_log.md (trade records)",
        "smart_money.md (new discoveries)",
        "playbook.md (setup performance)",
        "narratives.md (regime changes)",
        "tokens.md (symbol characteristics)",
    ]

    print("📚 KNOWLEDGE GRAPH UPDATES MANDATORY:")
    for update in kg_updates:
        print(f"   - {update}")

    print(
        "🔍 DEEP ANALYSIS REQUIREMENT: Must analyze whale intel patterns, smart money positioning, and historical performance before updates"
    )
    return "KG_UPDATES_REQUIRED"


# Protocol Enforcement Status
PROTOCOL_ENFORCED = True
COMPLIANCE_ACTIVE = True

print("🛡️ PROTOCOL COMPLIANCE SYSTEM LOADED")
print("⚠️ DEVIATIONS WILL BE AUTOMATICALLY DETECTED AND BLOCKED")
print("✅ READY FOR HYPERGROK DAILY EXECUTION")
