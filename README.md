# Agentic AI with AWS Bedrock AgentCore & Strands

A collection of hands-on examples for building and deploying agentic AI applications on **AWS Bedrock AgentCore** using the **Strands Agents** framework. This repo covers three progressively advanced patterns — from a simple "Hello World" agent to a fully authenticated agent secured with **Okta OAuth 2.0**.

---

## Examples Overview

| Example | File | Description |
|---------|------|-------------|
| 1. Basic Agent | `Hello_Hi_Agent_Strand.py` | Minimal agent that invokes Claude on Bedrock |
| 2. Weather Agent | `Weather_Agent_Strands.py` | Tool-enabled agent using Strands framework |
| 3. Support Agent + Okta Auth | `Support_Agent_Strand.py` + `invoke_AIAgent_okta_hello_world.sh` | Customer support agent with Okta JWT inbound authentication |

---

## Prerequisites

- Python 3.10+
- AWS account with Bedrock access enabled
- AWS CLI configured with a named profile (e.g., `agentic-ai`)
- AgentCore CLI installed (`bedrock-agentcore-starter-toolkit`)
- An Okta developer account (Example 3 only)
- Docker (for `agentcore launch`)

---

## Installation

```bash
git clone https://github.com/<your-username>/Agentic_AI_Bedrock_AgentCore_Introduction.git
cd Agentic_AI_Bedrock_AgentCore_Introduction
pip install -r requirements.txt
```

**requirements.txt includes:**
```
boto3>=1.40.13
fastapi>=0.116.1
uvicorn>=0.35.0
strands-agents>=1.5.0
bedrock-agentcore>=0.1.2
bedrock-agentcore-starter-toolkit>=0.1.6
strands-agents-tools>=0.2.4
```

---

## Example 1 — Basic Agent (`Hello_Hi_Agent_Strand.py`)

The simplest possible AgentCore integration. Sends a prompt directly to **Claude 3 Sonnet** on Amazon Bedrock and returns the response.

### Architecture

```
User Request → FastAPI /invoke → BedrockAgentCoreApp → Claude 3 Sonnet → Response
```

### Key Code

```python
from bedrock_agentcore.runtime import BedrockAgentCoreApp
import boto3, json

agentcore_app = BedrockAgentCoreApp()
bedrock_client = boto3.client('bedrock', region_name='us-east-1')

@agentcore_app.entrypoint
def invoke(payload):
    user_message = payload.get("prompt", "Hello")
    response = bedrock_client.invoke_model(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        body=json.dumps({"prompt": user_message, "max_tokens_to_sample": 300})
    )
    return json.loads(response['body'].read())['completion']
```

### Run Locally

```bash
python Hello_Hi_Agent_Strand.py
# Server starts on http://0.0.0.0:8080

# Test via curl
curl -X POST http://localhost:8080/invoke \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello! What can you do?"}'
```

### Deploy to AgentCore

```bash
export AWS_PROFILE=agentic-ai

agentcore configure \
  --name "hello_agent" \
  --entrypoint Hello_Hi_Agent_Strand.py \
  --execution-role arn:aws:iam::<ACCOUNT_ID>:role/<ROLE_NAME> \
  --ecr <ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/<ECR_REPO>

agentcore launch --local-build
agentcore invoke '{"prompt": "Hello!"}'
```

---

## Example 2 — Weather Agent with Tools (`Weather_Agent_Strands.py`)

Demonstrates the **Strands Agents** framework with custom tool use. The agent can answer questions about weather and perform math calculations using tools.

### Architecture

```
User Request → FastAPI /invoke → Strands Agent → [calculator | weather tools] → Claude Instant → Response
```

### Tools

| Tool | Source | Description |
|------|--------|-------------|
| `calculator` | `strands-agents-tools` | Performs math calculations |
| `weather` | Custom `@tool` decorator | Returns current weather (mock data) |

### Key Code

```python
from strands import Agent, tool
from strands_tools import calculator
from strands.models import BedrockModel

@tool
def weather():
    """Get weather"""
    return "It's sunny in Tokyo today."

model = BedrockModel(model_id="anthropic.claude-instant-v1")

agent = Agent(
    model=model,
    tools=[calculator, weather],
    system_prompt="You're a helpful assistant. You can do simple math calculations and tell the weather."
)

@agentcore_app.entrypoint
def strands_agent_bedrock(payload):
    user_input = payload.get("prompt", "Hello")
    response = agent(user_input)
    content = response.message.get("content", [])
    return content[0]["text"] if content else "No response."
```

### Run Locally

```bash
python Weather_Agent_Strands.py

# Ask about weather
curl -X POST http://localhost:8080/invoke \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is the weather in Tokyo?"}'

# Ask a math question
curl -X POST http://localhost:8080/invoke \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is 15 * 24?"}'
```

### Deploy to AgentCore

The included script `configure_weather_agentcore_strands.sh` automates the full configure + launch flow:

```bash
# Edit the script to match your AWS account and ECR repo, then:
chmod +x configure_weather_agentcore_strands.sh
./configure_weather_agentcore_strands.sh
```

Or manually:

```bash
agentcore configure \
  --name "weather_agent_strands" \
  --entrypoint Weather_Agent_Strands.py \
  --execution-role arn:aws:iam::<ACCOUNT_ID>:role/<ROLE_NAME> \
  --ecr <ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/weather_agent_strands \
  --requirements-file requirements.txt

agentcore launch --local-build
agentcore invoke '{"prompt": "What is the weather today?"}'
```

---

## Example 3 — Support Agent with Okta Inbound Authentication

A **customer support agent** secured with **Okta OAuth 2.0** (JWT) inbound authentication. Only clients presenting a valid Okta-issued bearer token can invoke the agent.

### Architecture

```
Client → Okta (client_credentials) → Access Token
       → agentcore invoke --bearer-token <token>
         → AgentCore (validates JWT via Okta discovery URL)
           → Support Agent (Amazon Titan Express) → Response
```

### The Agent (`Support_Agent_Strand.py`)

Handles e-commerce customer support with a custom return policy lookup tool:

```python
from strands import Agent, tool
from strands.models import BedrockModel

@tool
def get_return_policy(product_category: str) -> str:
    """Get return policy for a specific product category."""
    policies = {
        "electronics": "30-day return policy. Items must be in original packaging.",
        "clothing": "60-day return policy. Items must have tags attached and be unworn.",
        "books": "Returns accepted within 30 days if in good condition.",
        "home": "45-day return policy for home goods.",
        "beauty": "30-day return policy. Must be unopened for hygiene reasons."
    }
    return policies.get(product_category.lower(), "Standard 30-day return policy applies.")

agent = Agent(
    model=BedrockModel(model_id="amazon.titan-text-express-v1"),
    system_prompt="You are a professional customer support assistant for an e-commerce company..."
)

@app.entrypoint
def customer_support_agent(payload):
    response = agent(payload.get("prompt"))
    return response.message['content'][0]['text']
```

### Configuring Okta Authentication

**1. Create an Okta Application**
- Go to your Okta admin console
- Create a new **API Service** (machine-to-machine) application
- Note the `Client ID` and `Client Secret`
- Add a custom scope: `agent.invoke`

**2. Configure AgentCore Inbound Authorizer**

Create `inbound_authorizer.json` with your Okta OAuth settings:

```json
{
  "customJWTAuthorizer": {
    "discoveryUrl": "https://<YOUR_OKTA_DOMAIN>/oauth2/default/.well-known/openid-configuration",
    "allowedAudiences": ["api://default"],
    "allowedClients": ["<YOUR_OKTA_CLIENT_ID>"]
  }
}
```

Apply it when configuring your agent:

```bash
agentcore configure \
  --name "support_agent" \
  --entrypoint Support_Agent_Strand.py \
  --execution-role arn:aws:iam::<ACCOUNT_ID>:role/<ROLE_NAME> \
  --ecr <ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/support_agent \
  --inbound-auth inbound_authorizer.json

agentcore launch --local-build
```

**3. Invoke the Agent with Okta Authentication**

Use the included script `invoke_AIAgent_okta_hello_world.sh`:

```bash
# Edit the script with your Okta credentials, then:
chmod +x invoke_AIAgent_okta_hello_world.sh
./invoke_AIAgent_okta_hello_world.sh
```

The script performs two steps:

```bash
# Step 1: Get bearer token from Okta
ACCESS_TOKEN=$(curl -s --request POST \
  --url "https://${OKTA_DOMAIN}/oauth2/default/v1/token" \
  --header "Content-Type: application/x-www-form-urlencoded" \
  --user "${CLIENT_ID}:${CLIENT_SECRET}" \
  --data "grant_type=client_credentials&scope=agent.invoke" \
  | jq -r '.access_token')

# Step 2: Invoke the agent with the bearer token
agentcore invoke '{"prompt": "What is your return policy for electronics?"}' \
  --bearer-token "$ACCESS_TOKEN"
```

### Sample Interactions

```
Prompt: "What is your return policy for electronics?"
→ "Return Policy for Electronics: 30-day return policy for electronics.
   Items must be in original packaging with all accessories."

Prompt: "I have a question about a clothing return."
→ "Our clothing return policy allows returns within 60 days.
   Items must have tags attached and be unworn..."
```

---

## Project Structure

```
Agentic_AI_Bedrock_AgentCore_Introduction/
├── Hello_Hi_Agent_Strand.py              # Example 1: Basic agent
├── Weather_Agent_Strands.py              # Example 2: Tool-enabled weather agent
├── Support_Agent_Strand.py               # Example 3: Customer support agent
├── invoke_AIAgent_okta_hello_world.sh    # Okta auth invocation script
├── configure_weather_agentcore_strands.sh # AgentCore deployment script
├── inbound_authorizer.json               # IAM-based auth config
├── inbound_authorizer.json.Oauth.version # Okta OAuth auth config template
├── .bedrock_agentcore.yaml               # AgentCore agent configuration
├── requirements.txt
├── Getting_Started_Strands/              # Multi-agent travel system example
│   ├── shahzad_ai_agent1.py             # Travel Supervisor Agent
│   ├── shahzad_ai_agent2.py             # Flight Search Agent
│   └── shahzad_ai_agent3.py             # Hotel Search Agent
└── src/                                  # Shared utilities
    ├── tools.py                          # Tool definitions
    ├── utils.py                          # DynamoDB utilities
    ├── ssm_utils.py                      # AWS SSM Parameter Store helpers
    ├── rds_data_api_utils.py             # Aurora Serverless RDS Data API
    └── MemoryHookProvider.py             # Conversation memory management
```

---

## Key Technologies

| Technology | Role |
|-----------|------|
| **AWS Bedrock AgentCore** | Managed runtime for deploying agentic AI |
| **Strands Agents** | Python framework for building tool-enabled agents |
| **Claude 3 Sonnet / Claude Instant** | LLMs via Amazon Bedrock |
| **Amazon Titan Text** | LLM for customer support agent |
| **FastAPI** | HTTP server for local testing |
| **Okta OAuth 2.0** | Inbound JWT authentication for secure agent invocation |
| **AWS IAM** | Standard AWS-based authorization |

---

## AgentCore CLI Quick Reference

```bash
# Configure an agent
agentcore configure --name <name> --entrypoint <file.py> \
  --execution-role <ARN> --ecr <ECR_URI>

# Build and launch locally
agentcore launch --local-build

# Invoke the running agent
agentcore invoke '{"prompt": "your message here"}'

# Invoke with Okta bearer token
agentcore invoke '{"prompt": "your message here"}' --bearer-token <TOKEN>

# List deployed agent runtimes
aws bedrock-agentcore-control list-agent-runtimes --profile=agentic-ai
```

---

## Resources

- [AWS Bedrock AgentCore Documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-agentcore.html)
- [Strands Agents GitHub](https://github.com/strands-agents/sdk-python)
- [Strands Agents Tools](https://github.com/strands-agents/tools)
- [Okta Client Credentials Flow](https://developer.okta.com/docs/guides/implement-grant-type/clientcreds/main/)
