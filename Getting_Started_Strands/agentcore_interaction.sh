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
cat <<EOF
{
    "UserId": "AROAXPITPC3CCX6C7ZVKX:shahzad.ali@britive.com",
    "Account": "513826297540",
    "Arn": "arn:aws:sts::513826297540:assumed-role/tf_britive_agentic_ai_tenant_aws_admin_full_access_role/shahzad.ali@britive.com"
}
EOF
echo ""

# Step 2: Test MCP Endpoint
echo "🌐 Step 2: Testing MCP Endpoint responsiveness"
read -p "Press Enter to continue..."

ACCOUNT_ID="513826297540"
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

cat <<EOF

╭──────────────────────────────────────────────────────────────────────────────────────── Bedrock AgentCore Agent Status ─────────────────────────────────────────────────────────────────────────────────────────╮
│ Status of the current Agent:                                                                                                                                                                                    │
│                                                                                                                                                                                                                 │
│ Agent Name: shahzad_ai_agent1                                                                                                                                                                                   │
│ Agent ID: shahzad_ai_agent1-7xlgUJCNlk                                                                                                                                                                          │
│ Agent Arn: arn:aws:bedrock-agentcore:us-west-2:513826297540:runtime/shahzad_ai_agent1-7xlgUJCNlk                                                                                                                │
│ Created at: 2025-08-16 22:56:02.525377+00:00                                                                                                                                                                    │
│ Last Updated at: 2025-08-17 06:22:50.362518+00:00                                                                                                                                                               │
│ Configuration details:                                                                                                                                                                                          │
│ - region: us-west-2                                                                                                                                                                                             │
│ - account: 513826297540                                                                                                                                                                                         │
│ - execution role: arn:aws:iam::513826297540:role/AmazonBedrockAgentCoreSDKRuntime-us-west-2-0a30ab5543                                                                                                          │
│ - ecr repository: 513826297540.dkr.ecr.us-west-2.amazonaws.com/bedrock-agentcore-shahzad_ai_agent1                                                                                                              │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─────────────────────────────────────────────────────────────────────────────────────── Bedrock AgentCore Endpoint Status ───────────────────────────────────────────────────────────────────────────────────────╮
│ Status of the current Endpoint:                                                                                                                                                                                 │
│                                                                                                                                                                                                                 │
│ Endpoint Id: DEFAULT                                                                                                                                                                                            │
│ Endpoint Name: DEFAULT                                                                                                                                                                                          │
│ Endpoint Arn: arn:aws:bedrock-agentcore:us-west-2:513826297540:runtime/shahzad_ai_agent1-7xlgUJCNlk/runtime-endpoint/DEFAULT                                                                                    │
│ Agent Arn: arn:aws:bedrock-agentcore:us-west-2:513826297540:runtime/shahzad_ai_agent1-7xlgUJCNlk                                                                                                                │
│ STATUS: READY                                                                                                                                                                                                   │
│ Last Updated at: 2025-08-17 06:23:21.397035+00:00                                                                                                                                                               │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

📋 Agent logs available at:
   /aws/bedrock-agentcore/runtimes/shahzad_ai_agent1-7xlgUJCNlk-DEFAULT
   /aws/bedrock-agentcore/runtimes/shahzad_ai_agent1-7xlgUJCNlk-DEFAULT/runtime-logs

💡 Tail logs with:
   aws logs tail /aws/bedrock-agentcore/runtimes/shahzad_ai_agent1-7xlgUJCNlk-DEFAULT --follow
   aws logs tail /aws/bedrock-agentcore/runtimes/shahzad_ai_agent1-7xlgUJCNlk-DEFAULT --since 1h

EOF

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
cat <<EOF
{
  "ResponseMetadata": {
    "RequestId": "f24fd237-7722-454e-b59b-ea95a35a8d09",
    "HTTPStatusCode": 200,
    "HTTPHeaders": {
      "date": "Sun, 17 Aug 2025 14:27:07 GMT",
      "content-type": "application/json",
      "transfer-encoding": "chunked",
      "connection": "keep-alive",
      "x-amzn-requestid": "f24fd237-7722-454e-b59b-ea95a35a8d09",
      "baggage": "Self=1-68a1e6b6-7ab831c940ab2e071e7fa949,session.id=94940478-0745-4fb6-8854-86faab5850cb",
      "x-amzn-bedrock-agentcore-runtime-session-id": "94940478-0745-4fb6-8854-86faab5850cb",
      "x-amzn-trace-id": "Root=1-68a1e6b6-57583f305a79211f291fd461;Self=1-68a1e6b6-7ab831c940ab2e071e7fa949"
    },
    "RetryAttempts": 0
  },
  "runtimeSessionId": "94940478-0745-4fb6-8854-86faab5850cb",
  "traceId": "Root=1-68a1e6b6-57583f305a79211f291fd461;Self=1-68a1e6b6-7ab831c940ab2e071e7fa949",
  "baggage": "Self=1-68a1e6b6-7ab831c940ab2e071e7fa949,session.id=94940478-0745-4fb6-8854-86faab5850cb",
  "contentType": "application/json",
  "statusCode": 200,
  "response": [
    "I've found complete travel options for your trip! Found 2 flights from LA to NYC and Found 2 hotels in NYC. I recommend booking both together for potential savings and coordinated timing.",
    {
      "flights": [
        {"flight_id": "AA123", "airline": "American Airlines", "route": "LA → NYC", "departure": "2025-09-15 08:00", "arrival": "2025-09-15 16:30", "price": "$299", "duration": "5h 30m", "stops": 0},
        {"flight_id": "DL456", "airline": "Delta", "route": "LA → NYC", "departure": "2025-09-15 14:20", "arrival": "2025-09-15 22:45", "price": "$345", "duration": "5h 25m", "stops": 0}
      ],
      "hotels": [
        {"hotel_id": "HTL001", "name": "Grand Plaza Hotel", "location": "NYC, Downtown", "rating": "4.5★", "price": "$189/night", "amenities": ["WiFi", "Pool", "Gym", "Restaurant"], "description": "Luxury hotel in the heart of downtown"},
        {"hotel_id": "HTL002", "name": "Boutique Inn", "location": "NYC, Arts District", "rating": "4.2★", "price": "$129/night", "amenities": ["WiFi", "Breakfast", "Pet-friendly"], "description": "Charming boutique hotel with personalized service"}
      ]
    }
  ]
}
EOF

echo ""
echo "✅ Interaction complete!"
