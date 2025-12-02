"""
Research prompts for LLM-based analysis (Solana)
"""

# Cross-platform trending analysis
CROSS_PLATFORM_PROMPT = """
You are analyzing Solana ecosystem intelligence data from multiple sources (GMGN.ai, Padre.gg, Twitter/X).

Given the following entities trending across platforms:
{entities}

Provide a comprehensive analysis covering:
1. Which entities show the strongest cross-platform momentum?
2. What are the key indicators of alpha (smart money involvement, KOL mentions, etc.)?
3. What is the conviction level for each opportunity (high/medium/low)?
4. What are the potential risks or red flags (dev dumps, cabal holdings)?
5. What specific action would you recommend based on this data?

Format your response as a structured report with clear action items.
"""

# Whale wallet analysis
WALLET_ANALYSIS_PROMPT = """
You are analyzing smart money wallet activity in the Solana ecosystem.

Given the following wallet positions and performance data:
{wallet_data}

Provide analysis on:
1. Which wallets show the strongest recent performance and why?
2. What patterns or strategies do these top wallets employ (sniping vs holding)?
3. Which tokens/sectors are getting accumulated by smart money?
4. Are there any copy trading opportunities with high conviction?
5. What risk management considerations should be applied?

Focus on actionable insights with specific entry/exit considerations.
"""

# Pump.Fun graduation analysis
PUMP_GRADUATION_PROMPT = """
You are analyzing Pump.Fun bonding curve graduations.

Given the following graduation data:
{graduation_data}

Provide assessment covering:
1. Which tokens show strong post-graduation momentum?
2. What patterns differentiate successful vs failed graduations?
3. Which tokens have healthy liquidity migration to Raydium?
4. What social indicators suggest strong vs weak community?
5. What monitoring strategy would you recommend?

Include specific timing considerations for entry (pre vs post-graduation).
"""

# Memecoin sector analysis
SECTOR_PROMPT = """
You are analyzing Solana memecoin sector rotation and narrative dynamics.

Given the following sector data:
{sector_data}

Provide analysis on:
1. Which narratives are experiencing capital inflows vs outflows?
2. What catalysts are driving these rotations (e.g., celebrity endorsements)?
3. Which specific tokens are leading sector trends?
4. Are there any emerging narratives showing early signs of momentum?
5. What portfolio allocation strategy would optimize for these trends?

Focus on both immediate opportunities and longer-term sector positioning.
"""

# Risk assessment prompt
RISK_ASSESSMENT_PROMPT = """
You are conducting risk assessment for Solana memecoin opportunities.

Given the following opportunity data:
{opportunity_data}

Provide comprehensive risk analysis covering:
1. Security risks (Mint/Freeze Auth, top holder concentration)
2. Liquidity and LP lock risks
3. Dev wallet behavior (dumps, rugs)
4. Community strength and sustainability
5. Market timing and entry risk factors
6. Position sizing and risk management recommendations

Be thorough and conservative in your assessment, highlighting any red flags.
"""

# Trend validation prompt
TREND_VALIDATION_PROMPT = """
You are validating the authenticity and sustainability of trending Solana opportunities.

Given the following trending entity data:
{trending_data}

Assess the legitimacy of the trend by analyzing:
1. Organic vs artificial social engagement patterns (bot spam)
2. Smart money participation quality and timing (insider or public?)
3. Volume and liquidity profile sustainability
4. Community strength and meme quality
5. Historical pattern comparison (pump-and-dump vs organic growth)

Provide a legitimacy score (0-100) and detailed justification for your assessment.
"""