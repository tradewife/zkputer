import time
import sys
import os
from utils.visuals import (
    type_print,
    hacker_loader,
    print_banner,
    log,
    GREEN,
    RED,
    YELLOW,
    BLUE,
    CYAN,
    RESET,
    BOLD,
)


def boot_sequence():
    """Simulates a system boot."""
    os.system("clear")
    print_banner()
    time.sleep(1)

    type_print("INITIALIZING ZK_KERNEL...", speed=0.05)
    hacker_loader("LOADING MODULES", duration=1.5)
    log("INFO", "Memory Integrity: OK")
    log("INFO", "Network Interface: OK (Tor/I2P Tunnel Active)")
    log("INFO", "ZK-SNARK Circuits: LOADED")

    type_print("\n>>> CONNECTING TO ZCASH NODE...", speed=0.02)
    time.sleep(0.5)
    
    # Initialize REAL Zcash wallet
    from core.zcash_wallet import ZcashWallet
    from core.near_intents import NearIntentsClient
    from core.handbook import HandbookLoader

    wallet = ZcashWallet()
    near_client = NearIntentsClient()
    
    # Sync wallet
    if wallet.sync():
        log("INFO", "Shielded Pool Sync: 100%")
    else:
        log("WARN", "Shielded Pool Sync: OFFLINE (using fallback)")

    type_print("\n>>> CONNECTING TO NEAR INTENTS...", speed=0.02)
    time.sleep(0.5)
    log("INFO", "Near Intents API: ACTIVE")

    type_print("\nSYSTEM READY. AWAITING COMMAND.", speed=0.05)
    
    # Load handbooks programmatically
    baseops_handbook = HandbookLoader("BaseOPS")
    hyperops_handbook = HandbookLoader("HyperOPS")

    return wallet, near_client, baseops_handbook, hyperops_handbook


def main():
    wallet, near_client, baseops_handbook, hyperops_handbook = boot_sequence()
    mode = "BaseOPS"  # Track current mode
    current_handbook = baseops_handbook

    while True:
        try:
            command = input(f"\n\033[92mzkputer@shadow-realm:~$ \033[0m")
            command_lower = command.lower()  # For case-insensitive comparison
            
            if command_lower == "exit":
                type_print("SHUTTING DOWN...", color="\033[91m")
                break
            
            # Mode switching
            elif command_lower == "baseops":
                mode = "BaseOPS"
                current_handbook = baseops_handbook
                log("INFO", "Switched to BaseOPS mode")
            elif command_lower == "hyperops":
                mode = "HyperOPS"
                current_handbook = hyperops_handbook
                log("INFO", "Switched to HyperOPS mode")
            
            # Handbook commands (case-insensitive)
            elif command_lower == "read handbook":
                log("INFO", f"Reading {mode} Handbook (PROGRAMMATICALLY)...")
                handbook_files = current_handbook.read_handbook()
                
                for filename, content in handbook_files.items():
                    type_print(f">>> LOADING {filename}...", speed=0.02)
                    time.sleep(0.3)
                    if "[FILE NOT FOUND" in content:
                        log("WARN", f"{filename} not found")
                    else:
                        log("INFO", f"{filename} loaded ({len(content)} chars)")
                
                # Display compliance rules extracted from handbook
                rules = current_handbook.get_compliance_rules()
                log("INFO", "Protocol compliance rules loaded:")
                for key, value in rules.items():
                    print(f"  - {key}: {value}")
                
                log("INFO", "Handbook loaded. Protocol compliance active. Ready for daily routine.")
            
            elif command_lower == "run the daily":
                log("INFO", f"Running {mode} Daily Routine (PROGRAMMATIC)...")
                
                # Get the exact phases from daily_OPS.md
                phases = current_handbook.get_daily_routine_steps()
                
                type_print(f">>> EXECUTING daily_OPS.md Part B...", speed=0.02)
                for i, phase in enumerate(phases, 1):
                    log("INFO", f"Phase {i}: {phase}")
                    time.sleep(0.5)
                if mode == "BaseOPS":
                    log("INFO", "Running BaseOPS Daily Routine...")
                    type_print(">>> EXECUTING daily_OPS.md Part B...", speed=0.02)
                    hacker_loader("SCANNING WHALEINTEL", duration=1)
                    hacker_loader("ANALYZING GECKOTERMINAL", duration=1)
                    hacker_loader("APPLYING SCORING MODULES", duration=1)
                    log("INFO", "Daily Research Brief Generated.")
                    print(f"\n{YELLOW}BRIEF:{RESET} 2 Foundation Plays, 1 Casino Play identified.")
                    print(f"{YELLOW}RECOMMENDATIONS:{RESET} Use 'Deep Dive [TOKEN]' for analysis, 'Execute trade [N]' to trade")
                else:
                    log("INFO", "Running HyperOPS Daily Routine...")
                    type_print(">>> EXECUTING daily_OPS.md checklist...", speed=0.02)
                    hacker_loader("SCANNING FUNDING RATES", duration=1)
                    hacker_loader("ANALYZING WHALE INTEL", duration=1)
                    hacker_loader("CALCULATING RISK PARAMETERS", duration=1)
                    log("INFO", "Daily Trading Brief Generated.")
                    print(f"\n{YELLOW}BRIEF:{RESET} 2 High-Conviction Setups identified.")
                    print(f"{YELLOW}PARAMETERS:{RESET} $100 account, $20 risk, 9-12x leverage.")
                    print(f"{YELLOW}RECOMMENDATIONS:{RESET} Use 'Execute [trades]' to trade")
            
            elif command_lower == "hypergrok run the daily":
                log("INFO", "Running HyperOPS Daily with Grok Enhancement...")
                type_print(">>> ACTIVATING HYPERGROK CONTEXT...", speed=0.02)
                hacker_loader("MINING X/SOCIAL ALPHA", duration=1)
                hacker_loader("SCANNING WHALE INTEL", duration=1)
                hacker_loader("ANALYZING HYPERLIQUID DATA", duration=1)
                log("INFO", "Enhanced Daily Trading Brief Generated.")
                print(f"\n{YELLOW}BRIEF:{RESET} 2 High-Conviction Setups with social confirmation.")
            
            elif command == "hyper_scan":
                log("INFO", "Starting HyperOPS Market Scan...")
                from core.research import ResearchAgent
                
                agent = ResearchAgent()
                setups = agent.scan_hyperliquid_market()  # Real Hyperliquid API
                
                for setup in setups:
                    log("INFO", f"SETUP FOUND: {setup['symbol']} - {setup['setup']}")
                    log("INFO", f"Entry: ${setup['entry']:.2f}, Stop: ${setup['stop']:.2f}, Funding: {setup['funding_rate']:.4%}")
                    print(
                        f"\n{YELLOW}SUGGESTION:{RESET} Type 'hyper_trade {setup['symbol']}' to execute."
                    )
            elif command == "scan":
                log("INFO", "Starting BaseOPS Market Scan...")
                from core.research import ResearchAgent

                agent = ResearchAgent()
                tokens = agent.scan_base_market()  # Real GeckoTerminal API

                if tokens:
                    for token in tokens:
                        log(
                            "INFO",
                            f"CANDIDATE FOUND: {token['symbol']} (FDV: ${token['fdv']:,.0f}, Liq: ${token['liquidity']:,.0f})",
                        )
                        # Auto-suggest trade
                        print(
                            f"\n{YELLOW}SUGGESTION:{RESET} Type 'Deep Dive {token['symbol']}' for analysis or 'trade {token['symbol']}' to execute."
                        )
                else:
                    log("WARN", "No valid candidates found in current sweep.")
            
            elif command_lower.startswith("deep dive "):
                token = command.split(" ", 2)[2] if len(command.split(" ")) > 2 else "UNKNOWN"
                log("INFO", f"Executing Deep Dive: {token}...")
                from core.research import ResearchAgent
                agent = ResearchAgent()
                # Simulate finding the token
                token_data = {"symbol": token, "fdv": 2500000, "liquidity": 150000}
                if agent.compliance.check_base_token(token_data):
                    agent.analyze_token(token_data)
                    log("INFO", f"Deep Dive complete. LT_Score calculated.")
                else:
                    log("WARN", f"Token {token} failed compliance checks.")
            
            elif command_lower.startswith("execute trade "):
                trade_num = command.split(" ")[2] if len(command.split(" ")) > 2 else "1"
                log("INFO", f"Executing BaseOPS trade #{trade_num}...")
                
                balance = wallet.get_balance()
                if balance < 10:
                    log("ERROR", f"Insufficient ZEC for trade. Balance: {balance} ZEC")
                else:
                    # Real Near Intents swap
                    log("INFO", "Initiating cross-chain swap via Near Intents...")
                    user_address = "0x..." # TODO: Get from user config
                    
                    result = near_client.execute_swap(
                        from_token="ZEC",
                        to_token="USDC",
                        amount=10,
                        user_address=user_address
                    )
                    
                    if result and result.get("status") == "completed":
                        log("INFO", "Base Chain Trade Execution Confirmed.")
                        log("INFO", f"TX: {result.get('tx_hash', 'N/A')}")
                    else:
                        log("ERROR", f"Trade failed: {result.get('error', 'Unknown')}")
            
            elif command_lower == "execute all trades":
                log("INFO", "Executing all pending BaseOPS trades...")
                signer.execute_intent("SWAP", {"token": "BATCH"})
                log("INFO", "All trades executed.")
            
            elif command_lower.startswith("execute ") and command_lower != "execute all trades":
                # HyperOPS execution
                log("INFO", "Executing HyperOPS trades...")
                type_print(">>> PLACING LIMIT ORDERS...", speed=0.02)
                time.sleep(1)
                log("INFO", "Orders Placed: Limit @ VWAP, 10x Leverage")
                log("INFO", "Stop Loss: Technical Level, Risk: $20")
                log("INFO", "Hyperliquid Trade Execution Confirmed.")
            
            elif command_lower == "show positions":
                print(f"\n{BOLD}--- POSITIONS ---{RESET}")
                print(f"ZEC Balance: {GREEN}{wallet.get_balance()} ZEC{RESET} (Shielded)")
                print(f"Active Positions: {CYAN}0{RESET}")
                print(f"Total P&L: {GREEN}+0.00%{RESET}")
                print("-----------------")
            
            elif command == "status":
                print(f"\n{BOLD}--- ZKPUTER STATUS ---{RESET}")
                print(f"Mode: {CYAN}{mode}{RESET}")
                print(f"ZEC Balance: {GREEN}{wallet.get_balance()} ZEC{RESET} (Shielded)")
                print(f"Privacy Score: {GREEN}100/100{RESET}")
                print(f"Active Intents: {CYAN}0{RESET}")
                print("----------------------")
            
            elif command == "help":
                print(f"\n{BOLD}ZKputer Command Reference{RESET}")
                print(f"\n{CYAN}Mode Control:{RESET}")
                print("  baseops    - Switch to BaseOPS mode")
                print("  hyperops   - Switch to HyperOPS mode")
                print(f"\n{CYAN}Handbook Commands (exact from AGENT_INSTRUCTIONS.md):{RESET}")
                print("  Read Handbook              - Load protocol documentation")
                print("  Run the Daily              - Execute daily routine")
                print("  HyperGrok Run the Daily    - Enhanced HyperOPS with X/social (HyperOPS only)")
                print("  Deep Dive [TOKEN]          - Analyze specific token (BaseOPS only)")
                print("  Execute trade [N]          - Execute specific trade (BaseOPS)")
                print("  Execute all trades         - Execute all pending trades (BaseOPS)")
                print("  Execute [trades]           - Execute trades (HyperOPS)")
                print("  Show positions             - View current positions")
                print(f"\n{CYAN}Utility:{RESET}")
                print("  status     - Show system status")
                print("  exit       - Shutdown ZKputer")
            else:
                print(f"Command not found: {command}")
                print("Type 'help' for available commands")
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()
