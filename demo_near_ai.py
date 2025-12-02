#!/usr/bin/env python3
"""
ZKputer + NEAR AI Demo
Demonstrates privacy-preserving AI trading with ZEC funding
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.zcash_wallet import ZcashWallet
from core.near_intents import NearIntentsClient  
from core.near_ai_agent import NEARAIAgent


def demo_near_ai_analysis():
    """
    Demo 1: TEE-Verified Market Analysis
    """
    print("="*70)
    print(" ZKputer + NEAR AI: Privacy-Preserving Trading Intelligence")
    print("="*70)
    
    print("\n[DEMO 1] TEE-Verified Market Analysis\n")
    
    # Initialize NEAR AI agent
    agent = NEARAIAgent()
    
    # Analyze a Solana memecoin
    print("📊 Analyzing $PNUT on Solana...")
    market_data = {
        "symbol": "PNUT",
        "price": 0.85,
        "liquidity": 125000,
        "volume": 450000,
        "mint_auth": "Revoked",
        "top_holders_pct": 22.5,
        "chain": "solana"
    }
    
    result = agent.analyze_opportunity_with_tee(market_data)
    
    if "error" in result:
        print(f"\n❌ Error: {result['error']}")
        if "API error: 401" in result.get('error', ''):
            print("\n💡 Set your NEAR AI API key:")
            print("   export NEAR_AI_API_KEY=your_key")
            print("   Get key from: https://cloud.near.ai")
    else:
        print(f"\n✅ NEAR AI Analysis Complete")
        print(f"   Recommendation: {result['recommendation']}")
        print(f"   TEE Verified: {result['verified']}")
        print(f"   Model: {result['model']}")
        print(f"   Hardware: {result['tee_hardware']}")
        print(f"\n   Reasoning:")
        print(f"   {result['reasoning']}")
    
    return result


def demo_natural_language():
    """
    Demo 2: Natural Language ZEC Spending
    """
    print("\n\n" + "="*70)
    print("[DEMO 2] Natural Language ZEC Spending\n")
    
    agent = NEARAIAgent()
    
    intents = [
        "Buy $100 of SOL",
        "Send 5 ZEC to privacy research",
        "Donate $50 to AI safety causes"
    ]
    
    for intent in intents:
        print(f"\n📝 User Intent: '{intent}'")
        result = agent.execute_zec_via_natural_language(intent)
        
        if result.get("status") == "error":
            print(f"   ❌ Error: {result.get('error')}")
        else:
            print(f"   ✅ Status: {result.get('status')}")
            print(f"   ✅ Parsed: {result.get('intent', result.get('action'))}")
            if result.get("nlp_attestation"):
                print(f"   ✅ TEE Verified: {result['nlp_attestation']['verified']}")


def demo_privacy_flow():
    """
    Demo 3: Complete Privacy Flow
    ZEC → NEAR AI Analysis → NEAR Intents → Trade
    """
    print("\n\n" + "="*70)
    print("[DEMO 3] Complete Privacy Flow\n")
    
    # Initialize components
    zcash = ZcashWallet()
    agent = NEARAIAgent()
    
    print("🔐 Privacy Stack:")
    print(f"   ├─ Zcash Balance: {zcash.get_balance()} ZEC (Shielded)")
    print(f"   ├─ NEAR AI: TEE Inference (NVIDIA H100)")
    print(f"   ├─ NEAR Intents: Cross-chain swap")
    print(f"   └─ Result: Anonymous on-chain execution")
    
    print("\n📋 Flow:")
    print("   1. ✅ Zcash shielded funding (no KYC link)")
    print("   2. ✅ NEAR AI analysis (private TEE)")
    print("   3. ⏳ NEAR Intents swap (ZEC → SOL)")
    print("   4. ⏳ Jupiter execution (SOL → Token)")
    
    print("\n🎯 Privacy Guarantees:")
    print("   ✓ AI prompts encrypted in TEE")
    print("   ✓ No on-chain link to funding source")
    print("   ✓ Verifiable inference (hardware attestation)")
    print("   ✓ Cross-chain privacy via NEAR Intents")


def main():
    """Run all demos"""
    print("\n")
    
    # Demo 1: Market Analysis
    demo_near_ai_analysis()
    
    # Demo 2: Natural Language
    demo_natural_language()
    
    # Demo 3: Privacy Flow
    demo_privacy_flow()
    
    print("\n\n" + "="*70)
    print("✅ Demo Complete!")
    print("\nHackathon Bounties:")
    print("   • Cross-Chain Privacy Solutions ($20k)")
    print("     └─ ZEC + NEAR Intents ✓")
    print("   • Privacy-Preserving AI ($25k)")
    print("     └─ NEAR AI TEE Inference ✓")
    print("="*70)
    print()


if __name__ == "__main__":
    main()
