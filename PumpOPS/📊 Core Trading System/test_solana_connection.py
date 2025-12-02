import sys
import os

# Add current directory to path to allow imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from solana_trade_executor import SolanaTradeExecutor
from jupiter_swap_module import JupiterSwapModule

def test_connection():
    print("Testing Solana Connection...")
    try:
        executor = SolanaTradeExecutor()
        print(f"RPC URL: {executor.rpc_url}")
        
        # Test RPC connection by getting a random account or recent blockhash
        # For now, just checking if client initialization worked
        print("✅ Solana Client Initialized")
        
        # Check balance (will be 0 if no wallet loaded)
        balance = executor.get_balance()
        print(f"Wallet Balance: {balance} SOL")
        
    except Exception as e:
        print(f"❌ Solana Connection Failed: {e}")

def test_jupiter():
    print("\nTesting Jupiter API...")
    try:
        jupiter = JupiterSwapModule()
        # USDC to SOL quote
        usdc = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
        sol = "So11111111111111111111111111111111111111112"
        
        quote = jupiter.get_quote(usdc, sol, 1000000) # 1 USDC
        if quote:
            print(f"✅ Jupiter Quote Received: {quote.get('outAmount')} Lamports")
        else:
            print("❌ Jupiter Quote Failed (None returned)")
            
    except Exception as e:
        print(f"❌ Jupiter API Failed: {e}")

if __name__ == "__main__":
    test_connection()
    test_jupiter()
