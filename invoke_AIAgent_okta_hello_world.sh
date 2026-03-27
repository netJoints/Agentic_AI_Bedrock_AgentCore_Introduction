#!/bin/bash
set -e

# -------------------------------
# Configuration — set via environment variables or a .env file
# export OKTA_DOMAIN="your-domain.okta.com"
# export OKTA_CLIENT_ID="your-client-id"
# export OKTA_CLIENT_SECRET="your-client-secret"
# -------------------------------
OKTA_DOMAIN="${OKTA_DOMAIN:?Must set OKTA_DOMAIN}"
CLIENT_ID="${OKTA_CLIENT_ID:?Must set OKTA_CLIENT_ID}"
CLIENT_SECRET="${OKTA_CLIENT_SECRET:?Must set OKTA_CLIENT_SECRET}"
SCOPE="agent.invoke"
PROMPT_TEXT="${PROMPT_TEXT:-Hello}"

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
