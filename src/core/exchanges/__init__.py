"""
ZKputer Exchange Integrations
Unified interface for Extended, Hyperliquid, and Base (Coinbase CDP)
MAINNET ONLY - No testnet code paths
"""

import os
import json
from pathlib import Path
from typing import Dict, Optional
from dataclasses import dataclass
from dotenv import load_dotenv

CONFIG_DIR = Path("/home/kt/ZKputer/config/exchanges")


@dataclass
class ExchangeStatus:
    name: str
    configured: bool
    network: str
    error: Optional[str] = None


def load_extended_config() -> Dict:
    """Load Extended Exchange configuration"""
    config_path = CONFIG_DIR / "extended.json"
    if not config_path.exists():
        raise FileNotFoundError(f"Extended config not found: {config_path}")
    
    with open(config_path) as f:
        config = json.load(f)
    
    if config.get("testnet", True):
        raise ValueError("ABORT: Extended config has testnet=true. Mainnet only.")
    
    required = ["account_address", "api_key", "stark_public_key", "stark_private_key", "vault_number"]
    missing = [k for k in required if not config.get(k)]
    if missing:
        raise ValueError(f"Extended config missing: {missing}")
    
    return config


def load_hyperliquid_config() -> Dict:
    """Load Hyperliquid configuration"""
    config_path = CONFIG_DIR / "hyperliquid.json"
    if not config_path.exists():
        raise FileNotFoundError(f"Hyperliquid config not found: {config_path}")
    
    with open(config_path) as f:
        config = json.load(f)
    
    if config.get("testnet", True):
        raise ValueError("ABORT: Hyperliquid config has testnet=true. Mainnet only.")
    
    required = ["account_address", "secret_key"]
    missing = [k for k in required if not config.get(k)]
    if missing:
        raise ValueError(f"Hyperliquid config missing: {missing}")
    
    return config


def load_base_config() -> Dict:
    """Load Base/Coinbase CDP configuration from .env"""
    env_path = CONFIG_DIR / "base.env"
    if not env_path.exists():
        raise FileNotFoundError(f"Base config not found: {env_path}")
    
    load_dotenv(env_path)
    
    config = {
        "api_key_id": os.getenv("CDP_API_KEY_ID"),
        "api_key_secret": os.getenv("CDP_API_KEY_SECRET"),
        "network": os.getenv("CDP_NETWORK", "base-mainnet"),
    }
    
    if config["network"] != "base-mainnet":
        raise ValueError(f"ABORT: Base network is {config['network']}. Mainnet only.")
    
    if not config["api_key_id"] or not config["api_key_secret"]:
        raise ValueError("Base config missing CDP_API_KEY_ID or CDP_API_KEY_SECRET")
    
    return config


def verify_all_configs() -> Dict[str, ExchangeStatus]:
    """Verify all exchange configurations are valid and mainnet"""
    results = {}
    
    # Extended
    try:
        cfg = load_extended_config()
        results["extended"] = ExchangeStatus(
            name="Extended Exchange",
            configured=True,
            network="mainnet",
        )
        print(f"[OK] Extended: {cfg['account_address'][:10]}... vault={cfg['vault_number']}")
    except Exception as e:
        results["extended"] = ExchangeStatus(
            name="Extended Exchange",
            configured=False,
            network="unknown",
            error=str(e)
        )
        print(f"[FAIL] Extended: {e}")
    
    # Hyperliquid
    try:
        cfg = load_hyperliquid_config()
        results["hyperliquid"] = ExchangeStatus(
            name="Hyperliquid",
            configured=True,
            network="mainnet",
        )
        print(f"[OK] Hyperliquid: {cfg['account_address'][:10]}...")
    except Exception as e:
        results["hyperliquid"] = ExchangeStatus(
            name="Hyperliquid",
            configured=False,
            network="unknown",
            error=str(e)
        )
        print(f"[FAIL] Hyperliquid: {e}")
    
    # Base
    try:
        cfg = load_base_config()
        results["base"] = ExchangeStatus(
            name="Base (Coinbase CDP)",
            configured=True,
            network=cfg["network"],
        )
        print(f"[OK] Base: {cfg['api_key_id'][:12]}... network={cfg['network']}")
    except Exception as e:
        results["base"] = ExchangeStatus(
            name="Base (Coinbase CDP)",
            configured=False,
            network="unknown",
            error=str(e)
        )
        print(f"[FAIL] Base: {e}")
    
    # Summary
    all_ok = all(r.configured for r in results.values())
    print(f"\n{'='*50}")
    print(f"ALL EXCHANGES READY: {'YES' if all_ok else 'NO'}")
    
    return results


if __name__ == "__main__":
    verify_all_configs()
