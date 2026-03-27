#!/bin/bash
set -e  # Exit on any error

# Activate virtual environment
source /Users/shahzadali/Github/venv/bin/activate

# Set AWS profile (credentials will be fetched automatically via credential_process)
export AWS_PROFILE="agentic-ai"
echo "✅ AWS_PROFILE set to agentic-ai"

# Test credentials to ensure they work
echo "🔐 Testing AWS credentials..."
if ! aws sts get-caller-identity; then
    echo "❌ Failed to authenticate with AWS using profile: agentic-ai"
    exit 1
fi

# Change to agent directory
cd /Users/shahzadali/Library/CloudStorage/OneDrive-britive,Inc/Britive_Github/Bedrock_AgentCore_Agentic_AI

# Verify entrypoint file exists
ENTRYPOINT="Weather_Agent_Strands.py"
if [[ ! -f "$ENTRYPOINT" ]]; then
    echo "❌ Entrypoint file $ENTRYPOINT not found"
    exit 1
fi

# Define variables
EXECUTION_ROLE="arn:aws:iam::513826297540:role/service-role/AmazonBedrockAgentCoreRuntimeServiceRole-shahzad"
ECR_REPO="513826297540.dkr.ecr.us-west-2.amazonaws.com/weather_agent_strands"
REQUIREMENTS_FILE="requirements.txt"

# Run agentcore configure
echo "🚀 Running agentcore configure..."
agentcore configure \
  --name "weather_agent_strands" \
  --entrypoint "$ENTRYPOINT" \
  --execution-role "$EXECUTION_ROLE" \
  --ecr "$ECR_REPO" \
  --requirements-file "$REQUIREMENTS_FILE" \
  --verbose

# Launch agent
echo "🚀 Launching agentcore..."
#agentcore launch
agentcore launch --local-build 
