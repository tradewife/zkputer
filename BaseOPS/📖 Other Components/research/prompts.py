"""
Research prompts for LLM-based analysis
"""

# Cross-platform trending analysis
CROSS_PLATFORM_PROMPT = """
You are analyzing Base ecosystem intelligence data from multiple sources (GMGN, Cookie.fun, Kaito).

Given the following entities trending across platforms:
{entities}

Provide a comprehensive analysis covering:
1. Which entities show the strongest cross-platform momentum?
2. What are the key indicators of alpha (smart money involvement, social traction, etc.)?
3. What is the conviction level for each opportunity (high/medium/low)?
4. What are the potential risks or red flags?
5. What specific action would you recommend based on this data?

Format your response as a structured report with clear action items.
"""

# Whale wallet analysis
WALLET_ANALYSIS_PROMPT = """
You are analyzing smart money wallet activity in the Base ecosystem.

Given the following wallet positions and performance data:
{wallet_data}

Provide analysis on:
1. Which wallets show the strongest recent performance and why?
2. What patterns or strategies do these top wallets employ?
3. Which tokens/sectors are getting accumulated by smart money?
4. Are there any copy trading opportunities with high conviction?
5. What risk management considerations should be applied?

Focus on actionable insights with specific entry/exit considerations.
"""

# Pre-TGE project assessment
PRE_TGE_PROMPT = """
You are analyzing pre-TGE project mindshare and social momentum.

Given the following project data from Kaito:
{project_data}

Provide assessment covering:
1. Which projects show the strongest momentum and why?
2. What categories or themes are gaining traction?
3. Which projects have the highest potential for token launch success?
4. What social indicators suggest strong vs weak fundamentals?
5. What monitoring strategy would you recommend for these projects?

Include specific timing considerations and risk assessment.
"""

# AI agent sector analysis
AGENT_SECTOR_PROMPT = """
You are analyzing AI agent category rotation and sector dynamics.

Given the following agent category data:
{agent_data}

Provide analysis on:
1. Which categories are experiencing inflows vs outflows of mindshare?
2. What catalysts are driving these rotations?
3. Which specific agents are leading category trends?
4. Are there any emerging categories showing early signs of momentum?
5. What portfolio allocation strategy would optimize for these trends?

Focus on both immediate opportunities and longer-term sector positioning.
"""

# Risk assessment prompt
RISK_ASSESSMENT_PROMPT = """
You are conducting risk assessment for Base ecosystem opportunities.

Given the following opportunity data:
{opportunity_data}

Provide comprehensive risk analysis covering:
1. Smart contract and security risks
2. Liquidity and market structure risks
3. Regulatory and compliance considerations
4. Team and founder due diligence concerns
5. Market timing and entry risk factors
6. Position sizing and risk management recommendations

Be thorough and conservative in your assessment, highlighting any red flags.
"""

# Trend validation prompt
TREND_VALIDATION_PROMPT = """
You are validating the authenticity and sustainability of trending opportunities.

Given the following trending entity data:
{trending_data}

Assess the legitimacy of the trend by analyzing:
1. Organic vs artificial social engagement patterns
2. Smart money participation quality and timing
3. Volume and liquidity profile sustainability
4. Community strength and project fundamentals
5. Historical pattern comparison and anomaly detection

Provide a legitimacy score (0-100) and detailed justification for your assessment.
"""