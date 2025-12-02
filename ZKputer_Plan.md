# ZKputer: The Sovereign Shadow Trader

## 🎯 Goal
Win the **Zypherpunk Hackathon** (Private DeFi & Cross-Chain Tracks) by building **ZKputer**: A fully-private, autonomous AI trading agent running inside its own virtual Linux desktop, funded by Zcash, and executing cross-chain via Near Intents.

## 💡 The "Banger" Concept
**"Ghost in the Shell... with a Pilot"**

Imagine a trading agent that doesn't just run as a script in the background, but "lives" in a private, visual computer. You don't send it API keys; you fund it with Zcash. It doesn't use your wallet; it uses Chain Signatures to trade anywhere.

**Iteration 1 (The Cyborg):** You log into the desktop and see the agent working. You see terminal windows flying open, code scrolling, charts loading. It finds a setup, but it waits for you. "Captain, permission to engage?" You type "YES". It executes via Near Intents.

**Iteration 2 (The Ghost):** You log out. The agent continues. It learns from your decisions in Iteration 1 and begins to operate fully autonomously.

**The Killer Demo:** A web interface showing a retro-futuristic Linux desktop (The ZKputer). You see the agent "typing" research, presenting a trade, and the human user approving it. It feels like watching a hacker team at work.

## 🏗 System Architecture

### 1. The Privacy Layer (Zcash)
*   **Role:** Funding & Settlement.
*   **Mechanism:** The ZKputer has a Zcash Shielded Address. The user funds it with ZEC.
*   **Why:** Breaks the on-chain link between the user's main assets and the trading bot's operations.

### 2. The Execution Layer (Near Intents / Chain Signatures)
*   **Role:** Universal Action.
*   **Mechanism:** The ZKputer controls a Near account with **Chain Signatures**.
*   **Capability:** It can sign transactions for **Base** (EVM), **Hyperliquid**, **Bitcoin**, and **Solana** without holding native gas tokens (using Near for gas abstraction or intents).
*   **Why:** Allows the agent to be "Chain Agnostic" and maintain privacy (no funding of ETH wallets from a KYC'd exchange).

### 3. The Brain (AI Agent)
*   **Role:** Strategy & Logic.
*   **Core:**
    *   **PumpOPS:** Solana Sniping (Pump.fun / Jupiter).
    *   **BaseOPS:** Base Chain Gem Discovery.
    *   **HyperOPS:** Hyperliquid Perp Trading.
*   **Upgrade:** Runs locally within the ZKputer environment.
*   **Tech:** Python, LLM (Gemini/Grok via API), specialized "Agent Tools" for the virtual desktop.

### 4. The Body (Virtual Linux Desktop)
*   **Role:** The Runtime & Interface.
*   **Tech:** Docker container running **XFCE** or **i3** window manager + **noVNC** (HTML5 VNC Viewer).
*   **Aesthetics:** Custom "Cyberpunk/Hacker" theme (Green/Black terminal, neon borders, glitch effects).
*   **Visibility:** The user accesses `localhost:6080` (or a deployed URL) to "watch" the agent work.

## 🗺 Implementation Roadmap

### Phase 1: The Shell (Virtual Desktop)
*   Create a Dockerfile with a lightweight Linux Desktop (Alpine + XFCE).
*   Install `noVNC` for browser access.
*   Style it: "Zypherpunk" wallpaper, custom terminal colors.
*   **Deliverable:** A browser-accessible Linux desktop that looks cool.

### Phase 2: The Brain (Agent Port)
*   Clone `BaseOPS`, `PumpOPS`, and `HyperOPS` logic into the container.
*   Modify `daily_OPS.py` to run "visually" (e.g., open a terminal window for each step, print logs slowly for effect).
*   **Deliverable:** The agent runs inside the desktop and you can see it "typing".

### Phase 3: The Hands (Real Privacy & Execution)
*   **Zcash Integration:**
    *   Implemented `src/core/zcash_wallet.py` wrapping `zecwallet-cli`.
    *   Enables real shielded sync, balance checks, and transfers.
*   **Near Intents:**
    *   Implemented `src/core/near_intents.py` using the HTTP API.
    *   Enables cross-chain swaps (ZEC -> SOL/USDC) via intent solvers.
*   **Deliverable:** The agent can actually sign a transaction on Base/Solana using ZEC funding.

### Phase 4: The Polish (Demo Mode)
*   Create a "Demo Script" that runs a full loop:
    1.  Receive ZEC (Real Shielded Tx).
    2.  Open Terminal: "ANALYZING MARKET..."
    3.  Open Browser (in VM): Load GeckoTerminal / Padre.gg.
    4.  Open Terminal: "OPPORTUNITY DETECTED: $DEGEN"
    5.  Execute Trade via Near Intents.
    6.  Display "PROFIT SECURED".
*   **Deliverable:** A 2-minute video recording of the ZKputer in action.

## 🛠 Tech Stack
*   **Languages:** Python, Bash, HTML/CSS (for VNC skin).
*   **Infrastructure:** Docker, `zecwallet-cli`, Near Intents API.
*   **AI:** Gemini Pro / Grok (via API).

## 🏆 Hackathon Tracks
*   **Private DeFi & Trading:** The core use case.
*   **Cross-Chain Privacy:** Using Near to trade on Base/Hyperliquid/Solana privately.
*   **Zcash Integration:** Funding layer.
