#!/bin/bash

# Title
echo "======================================"
echo "🧠 Bedrock AgentCore Interaction Script"
echo "======================================"
echo ""

# Step 1: Get AWS Caller Identity
echo "🔍 Step 1: Verifying AWS Identity using profile 'agentic-ai'"
read -p "Press Enter to continue..."
echo ""
echo "Command: aws sts get-caller-identity --profile agentic-ai"
echo ""
aws sts get-caller-identity --profile agentic-ai
echo ""

# Step 2: Test MCP Endpoint
echo "🌐 Step 2: Testing MCP Endpoint responsiveness"
read -p "Press Enter to continue..."

ACCOUNT_ID=$(aws sts get-caller-identity --profile agentic-ai --output text --query Account)
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCOUNT_ID" \
  "https://shahzad-travel-gateway-bwyyovtxbf.gateway.bedrock-agentcore.us-west-2.amazonaws.com/mcp" \
  -d '{"jsonrpc": "2.0", "method": "initialize", "params": {}, "id": 1}'

echo ""
echo "⚠️ Note: You may see an 'Invalid Bearer token' error if the token is not authorized."
echo ""

# Step 3: Check AgentCore Status
echo "📊 Step 3: Checking AgentCore Status"
read -p "Press Enter to continue..."
agentcore status


# Step 4: Invoke Agent with Prompt
echo "🚀 Step 4: Invoking Bedrock AgentCore agent 'shahzad_ai_agent1'"
read -p "Press Enter to continue..."

PROMPT='{"prompt": "Plan a trip from LA to NYC"}'
echo "Payload:"
echo "$PROMPT"
echo ""

echo "Invoking agent..."
echo "Session ID: 94940478-0745-4fb6-8854-86faab5850cb"
echo ""

# Real-time response from agent
echo "Response:"

echo ""
echo "✅ Interaction complete!"
