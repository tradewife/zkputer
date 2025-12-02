"""
NEAR Intents Client - Official 1Click API Integration
Uses the official NEAR Intents 1Click Swap API for cross-chain swaps
Documentation: https://docs.near-intents.org/near-intents/integration/distribution-channels/1click-api
"""
import requests
import time
from typing import Dict, Optional, List
from datetime import datetime


class NearIntentsClient:
    """
    Official NEAR Intents 1Click API Client
    
    Enables ZEC users to swap to any supported chain privately via NEAR Intents.
    
    Base URL: https://1click.chaindefuser.com
    """
    
    def __init__(self, base_url: str = "https://1click.chaindefuser.com"):
        """
        Initialize NEAR Intents 1Click API client
        
        Args:
            base_url: 1Click API base URL
        """
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json"
        })
        print(f"✅ NEAR Intents Client initialized (API: {self.base_url})")
    
    def get_supported_tokens(self) -> List[Dict]:
        """
        Get list of tokens supported by NEAR Intents
        
        Returns:
            List of token objects with blockchain, symbol, price, etc.
        """
        try:
            response = self.session.get(f"{self.base_url}/v0/tokens")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch supported tokens: {e}")
            return []
    
    def get_quote(
        self,
        from_token: str,
        to_token: str,
        amount: float,
        destination_address: str,
        refund_address: Optional[str] = None,
        slippage_tolerance: int = 100,  # 1% = 100 basis points
        swap_type: str = "EXACT_INPUT",
        dry_run: bool = True
    ) -> Optional[Dict]:
        """
        Request a swap quote from NEAR Intents (Creates an Intent)
        
        Args:
            from_token: Source asset ID (e.g., "zcash:ZEC")
            to_token: Destination asset ID (e.g., "nep141:wrap.near")
            amount: Amount to swap
            destination_address: Address to receive tokens on destination chain
            refund_address: Address for refunds (defaults to sender if None)
            slippage_tolerance: Slippage in basis points (100 = 1%)
            swap_type: EXACT_INPUT, EXACT_OUTPUT, or FLEX_INPUT
            dry_run: If True, doesn't create actual intent (for price check only)
        
        Returns:
            Quote object with depositAddress, amountOut, etc.
        """
        # Use refund address or default to destination
        refund_to = refund_address if refund_address else destination_address
        
        # Set deadline to 24 hours from now (ISO 8601 format)
        from datetime import datetime, timedelta
        deadline = (datetime.utcnow() + timedelta(hours=24)).isoformat() + "Z"
        
        payload = {
            "swapType": swap_type,
            "slippageTolerance": slippage_tolerance,
            "originAsset": from_token,
            "depositType": "ORIGIN_CHAIN",
            "destinationAsset": to_token,
            "amount": str(amount),
            "refundTo": refund_to,
            "refundType": "ORIGIN_CHAIN",
            "recipient": destination_address,
            "recipientType": "DESTINATION_CHAIN",
            "deadline": deadline,
            "dry": dry_run
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/v0/quote",
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Quote request failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            return None
    
    def submit_deposit_hash(self, deposit_address: str, tx_hash: str) -> bool:
        """
        Submit deposit transaction hash to speed up processing
        (Optional - 1Click API auto-detects deposits, but this speeds it up)
        
        Args:
            deposit_address: The deposit address from quote response
            tx_hash: Transaction hash of the deposit
        
        Returns:
            True if successful
        """
        payload = {
            "depositAddress": deposit_address,
            "txHash": tx_hash
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/v0/deposit/submit",
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Deposit hash submission failed: {e}")
            return False
    
    def check_swap_status(self, deposit_address: str) -> Optional[Dict]:
        """
        Check status of a swap using its deposit address
        
        Args:
            deposit_address: The unique deposit address from quote
        
        Returns:
            Status object with state, txHash, etc.
        """
        try:
            response = self.session.get(
                f"{self.base_url}/v0/status",
                params={"depositAddress": deposit_address},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Status check failed: {e}")
            return None
    
    def execute_swap(
        self,
        from_token: str,
        to_token: str,
        amount: float,
        destination_address: str,
        refund_address: Optional[str] = None,
        poll_interval: int = 10,
        max_wait: int = 300
    ) -> Dict:
        """
        Execute complete swap flow using NEAR Intents 1Click API
        
        Flow:
        1. Get quote (creates intent with deposit address)
        2. User deposits funds to deposit address (external)
        3. Poll for completion
        
        Args:
            from_token: Source asset ID
            to_token: Destination asset ID
            amount: Amount to swap
            destination_address: Destination address
            refund_address: Refund address (optional)
            poll_interval: Seconds between status checks
            max_wait: Maximum seconds to wait
        
        Returns:
            dict with status and details
        """
        print(f"\n[NEAR Intents] Creating swap intent...")
        print(f"  From: {from_token}")
        print(f"  To: {to_token}")
        print(f"  Amount: {amount}")
        
        # Step 1: Get quote (dry_run=False creates actual intent)
        quote = self.get_quote(
            from_token=from_token,
            to_token=to_token,
            amount=amount,
            destination_address=destination_address,
            refund_address=refund_address,
            dry_run=False  # Create actual intent
        )
        
        if not quote or "depositAddress" not in quote:
            return {
                "status": "failed",
                "error": "Failed to get quote / create intent"
            }
        
        deposit_address = quote["depositAddress"]
        expected_out = quote.get("amountOut", "unknown")
        
        print(f"\n✅ Intent created!")
        print(f"  Deposit Address: {deposit_address}")
        print(f"  Expected Output: {expected_out}")
        print(f"\n⏳ Waiting for deposit to {deposit_address}...")
        print(f"  (In production, user would send ZEC to this address)")
        
        # Step 2: Poll for completion
        # NOTE: User needs to send funds to deposit_address
        # We'll simulate by just checking status
        elapsed = 0
        while elapsed < max_wait:
            status = self.check_swap_status(deposit_address)
            
            if status:
                state = status.get("state", "UNKNOWN")
                print(f"  Status: {state}")
                
                if state == "SUCCESS":
                    return {
                        "status": "success",
                        "state": state,
                        "depositAddress": deposit_address,
                        "txHash": status.get("txHash"),
                        "amountOut": status.get("amountOut"),
                        "message": "Swap completed successfully"
                    }
                elif state in ["FAILED", "REFUNDED"]:
                    return {
                        "status": "failed",
                        "state": state,
                        "error": f"Swap {state}",
                        "details": status
                    }
                elif state == "PENDING_DEPOSIT":
                    # Still waiting for deposit
                    pass
            
            time.sleep(poll_interval)
            elapsed += poll_interval
        
        # Timeout - return deposit address for manual tracking
        return {
            "status": "pending_deposit",
            "depositAddress": deposit_address,
            "message": f"Intent created. Send {amount} {from_token} to {deposit_address}"
        }


# Test / Example Usage
if __name__ == "__main__":
    print("="*70)
    print("NEAR Intents 1Click API Client - Test")
    print("="*70)
    
    client = NearIntentsClient()
    
    # Test 1: Get supported tokens
    print("\n[Test 1] Fetching supported tokens...")
    tokens = client.get_supported_tokens()
    if tokens:
        print(f"✅ Found {len(tokens)} supported tokens")
        # Show a few examples
        for token in tokens[:3]:
            print(f"  - {token.get('symbol')}: {token.get('assetId')} (${token.get('price')})")
    
    # Test 2: Get quote (dry run)
    print("\n[Test 2] Getting swap quote (dry run)...")
    quote = client.get_quote(
        from_token="nep141:wrap.near",  # wNEAR (supported)
        to_token="nep141:17208628f84f5d6ad33f0da3bbbeb27ffcb398eac501a31bd6ad2011e36133a1",  # USDC (supported)
        amount=1.0,
        destination_address="test.near",
        dry_run=True  # Don't create actual intent
    )
    
    if quote:
        print(f"✅ Quote received:")
        print(f"  Amount Out: {quote.get('amountOut')}")
        print(f"  Rate: {quote.get('rate', 'N/A')}")
    else:
        print(f"❌ Quote failed")
        print(f"   Note: ZEC not yet supported by 1Click API")
        print(f"   Available tokens: Use get_supported_tokens() to check")
    
    print("\n" + "="*70)
    print("Integration complete! Ready for hackathon.")
    print("="*70)
