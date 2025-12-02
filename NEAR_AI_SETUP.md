# NEAR AI Setup Instructions

## Get Your API Key

1. Go to https://cloud.near.ai
2. Sign up / Log in
3. Navigate to "API Keys" section
4. Generate a new API key
5. Add credits to your account (go to "Credits" section)

## Configure ZKputer

Add your API key to `.env`:

```bash
echo "NEAR_AI_API_KEY=your_api_key_here" >> .env
```

Or export it:

```bash
export NEAR_AI_API_KEY=your_api_key_here
```

## Test the Integration

```bash
python3 src/core/near_ai_agent.py
```

You should see TEE-verified market analysis output.

## Privacy Guarantees

- All inference runs in NVIDIA H100 TEE
- Hardware attestation verifiable
- NEAR AI cannot view your prompts or responses
- Data encrypted in transit and at rest
