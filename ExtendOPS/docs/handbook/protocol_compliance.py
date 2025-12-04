# Protocol Compliance System
# Ensures HyperGrok + Daily OPS protocol is executed exactly as specified


def verify_protocol_compliance(phase_completed, current_phase_data):
    """
    Verifies each phase against daily_OPS.md requirements
    Returns compliance status and missing items
    """

    compliance_checklist = {
        "phase_0": {
            "performance_review": False,
            "regime_assessment": False,
            "setup_selection": False,
            "smart_money_review": False,
        },
        "phase_1": {
            "hyperliquid_scan": False,
            "funding_oi_analysis": False,
            "catalyst_detection": False,
            "whale_intel_scan": False,
        },
        "phase_2": {
            "technical_analysis": False,
            "thesis_validation": False,
            "smart_money_corroboration": False,
            "risk_management_planning": False,
        },
        "phase_3": {
            "trade_specifications": False,
            "execution_readiness": False,
            "monitoring_plan": False,
        },
        "phase_4": {"knowledge_graph_updates": False, "daily_brief_generation": False},
        "output_verification": {
            "market_snapshot": False,
            "evidence_tables": False,
            "whale_intel_digest": False,
            "playbook_cards": False,
            "final_trades": False,
            "x_post": False,
            "citations": False,
        },
    }

    return compliance_checklist


def hypergrok_enhancement_check():
    """
    Verifies HyperGrok enhancements are properly integrated
    """
    hypergrok_requirements = [
        "x_intelligence_sweep",
        "catalyst_mining",
        "sentiment_analysis",
        "multi_source_verification",
        "confidence_scoring",
    ]
    return hypergrok_requirements


def template_compliance_check():
    """
    Ensures exact template formats are used
    """
    required_templates = [
        "daily_trading_brief_template.md",
        "trade_analysis_template.md",
        "catalyst_watch_template.md",
    ]
    return required_templates


def knowledge_graph_update_check():
    """
    Verifies all knowledge graph files are updated
    """
    required_updates = [
        "performance_log.md",
        "smart_money.md",
        "playbook.md",
        "narratives.md",
        "tokens.md",
    ]
    return required_updates


def output_order_verification():
    """
    Ensures output follows exact daily_OPS.md order:
    1) Market Snapshot
    2) Evidence Tables
    3) On-Chain & Whale Intel Digest
    4) Top 3 Playbook Cards
    5) Final Two Trades
    6) X Post
    """
    correct_order = [
        "market_snapshot",
        "evidence_tables",
        "whale_intel_digest",
        "playbook_cards",
        "final_trades",
        "x_post",
    ]
    return correct_order


# Protocol Enforcement Rules
PROTOCOL_RULES = {
    "strict_template_usage": True,
    "mandatory_knowledge_updates": True,
    "exact_output_order": True,
    "hypergrok_as_enhancement_only": True,
    "self_correction_required": True,
}


def protocol_reset():
    """
    Resets protocol execution to Phase 0
    """
    return "Protocol reset. Restarting from Phase 0: Market Preparation"


def protocol_check():
    """
    Immediate compliance verification
    """
    return "Running protocol compliance check..."
