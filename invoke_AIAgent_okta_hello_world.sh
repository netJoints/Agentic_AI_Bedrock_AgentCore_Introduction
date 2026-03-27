#!/bin/bash
# Activate virtual environment
source /Users/shahzadali/Github/venv/bin/activate
aws bedrock-agentcore-control list-agent-runtimes --profile=agentic-ai

# -------------------------------
# Configuration
# -------------------------------
OKTA_DOMAIN="trial-3508361.okta.com"
CLIENT_ID="0oaugi5fw5DYbhq94697"
CLIENT_SECRET="KnmeRqGlLCkSt7JhKG9UQiX2w4vIfeIaBff4fp9KErpc4Zi8PvYyzOxSnSZme5rD"
SCOPE="agent.invoke"
PROMPT_TEXT="Hello"

# -------------------------------
# Step 1: Get Bearer Token from Okta
# -------------------------------
echo "Requesting bearer token from Okta..."
ACCESS_TOKEN=$(curl -s --request POST \
  --url "https://${OKTA_DOMAIN}/oauth2/default/v1/token" \
  --header "Accept: application/json" \
  --header "Content-Type: application/x-www-form-urlencoded" \
  --user "${CLIENT_ID}:${CLIENT_SECRET}" \
  --data "grant_type=client_credentials&scope=${SCOPE}" \
  | jq -r '.access_token')

# Check if token was obtained
if [ -z "$ACCESS_TOKEN" ] || [ "$ACCESS_TOKEN" == "null" ]; then
  echo "Failed to get access token from Okta."
  exit 1
fi

echo "Access token obtained successfully."

# -------------------------------
# Step 2: Invoke AgentCore with the token
# -------------------------------
echo "Invoking agentcore with prompt: $PROMPT_TEXT"
agentcore invoke "{
  \"prompt\": \"${PROMPT_TEXT}\"
}" --bearer-token "$ACCESS_TOKEN"
