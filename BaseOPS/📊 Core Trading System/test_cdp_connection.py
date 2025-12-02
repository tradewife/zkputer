#!/usr/bin/env python3
"""
Test CDP Connection
Verifies CDP credentials and creates a test wallet
"""

import sys
import os

# Add config path to load .env
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '⚙️ Configuration', 'config'))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '⚙️ Configuration', 'config', '.env'))

try:
    from cdp_client import CDPClient
    
    print("=" * 60)
    print("🧪 Testing CDP Connection")
    print("=" * 60)
    
    # Initialize CDP client
    client = CDPClient(network="base-mainnet")
    
    # Create a test wallet
    print("\n📝 Creating test wallet...")
    wallet = client.create_wallet()
    
    # Get wallet address
    address = client.get_address()
    print(f"✅ Wallet Address: {address}")
    
    # Check balances
    print(f"\n💰 Checking balances...")
    eth_balance = client.get_balance("eth")
    print(f"   ETH: {eth_balance}")
    
    usdc_balance = client.get_balance("usdc")
    print(f"   USDC: {usdc_balance}")
    
    # Export wallet for backup
    print(f"\n💾 Exporting wallet data...")
    wallet_data = client.export_wallet()
    
    # Save wallet backup
    backup_path = os.path.join(os.path.dirname(__file__), '..', '..', '⚙️ Configuration', 'config', 'wallet_backup.json')
    with open(backup_path, 'w') as f:
        f.write(wallet_data)
    print(f"✅ Wallet backed up to: {backup_path}")
    print(f"   ⚠️  Keep this file secure!")
    
    print("\n" + "=" * 60)
    print("✅ CDP Connection Successful!")
    print("=" * 60)
    print(f"\n📍 Your Base Wallet Address: {address}")
    print(f"\n🎯 Next Steps:")
    print(f"   1. Fund this wallet with USDC on Base chain")
    print(f"   2. Start trading via BaseOPS daily routine")
    print(f"   3. Keep wallet_backup.json safe!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print(f"\n🔧 Troubleshooting:")
    print(f"   1. Check CDP_API_KEY_NAME in .env")
    print(f"   2. Check CDP_PRIVATE_KEY in .env")
    print(f"   3. Verify credentials at portal.cdp.coinbase.com")
    sys.exit(1)
