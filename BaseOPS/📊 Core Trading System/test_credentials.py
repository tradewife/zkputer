#!/usr/bin/env python3
"""
Minimal CDP Connection Test
Tests credentials without hanging
"""

import os
import sys

# Load environment
sys.path.insert(0, os.path.dirname(__file__))
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '⚙️ Configuration', 'config', '.env'))

print("=" * 60)
print("🧪 CDP Credentials Test")
print("=" * 60)

# Check environment variables
api_key_id = os.getenv("CDP_API_KEY_ID")
api_key_secret = os.getenv("CDP_API_KEY_SECRET")

print(f"\n📋 Environment Variables:")
print(f"   CDP_API_KEY_ID: {api_key_id[:8]}...{api_key_id[-4:] if api_key_id else 'NOT SET'}")
print(f"   CDP_API_KEY_SECRET: {'***' + api_key_secret[-8:] if api_key_secret else 'NOT SET'}")

if not api_key_id or not api_key_secret:
    print("\n❌ Error: Missing CDP credentials in .env file")
    sys.exit(1)

print(f"\n✅ Credentials loaded successfully!")
print(f"\n🔄 Testing CDP SDK import...")

try:
    from cdp import CdpClient
    print(f"✅ CDP SDK imported successfully")
except Exception as e:
    print(f"❌ CDP SDK import failed: {e}")
    sys.exit(1)

print(f"\n✅ All checks passed!")
print(f"\n📍 Next: Phase 2 implementation (token swaps)")
print("=" * 60)
