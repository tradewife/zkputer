import requests
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("JupiterSwapModule")

class JupiterSwapModule:
    def __init__(self, api_url: str = "https://quote-api.jup.ag/v6"):
        self.api_url = api_url

    def get_quote(self, input_mint: str, output_mint: str, amount: int, slippage_bps: int = 50) -> Optional[Dict[str, Any]]:
        url = f"{self.api_url}/quote"
        params = {
            "inputMint": input_mint,
            "outputMint": output_mint,
            "amount": amount,
            "slippageBps": slippage_bps
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get quote from Jupiter: {e}")
            return None

    def get_swap_transaction(self, quote_response: Dict[str, Any], user_public_key: str) -> Optional[str]:
        url = f"{self.api_url}/swap"
        payload = {
            "quoteResponse": quote_response,
            "userPublicKey": user_public_key,
            "wrapAndUnwrapSol": True
        }
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json().get("swapTransaction")
        except Exception as e:
            logger.error(f"Failed to get swap transaction from Jupiter: {e}")
            return None
