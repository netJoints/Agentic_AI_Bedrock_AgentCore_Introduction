from fastapi import FastAPI, Request
from bedrock_agentcore.runtime import BedrockAgentCoreApp
import boto3
import json

# Initialize FastAPI and AgentCore
fastapi_app = FastAPI()
agentcore_app = BedrockAgentCoreApp()
bedrock_client = boto3.client('bedrock', region_name='us-east-1')

# Health check endpoint required by AgentCore
@fastapi_app.get("/health")
async def health():
    return {"status": "ok"}

# AgentCore entrypoint
@agentcore_app.entrypoint
def invoke(payload):
    user_message = payload.get("prompt", "Hello")
    try:
        response = bedrock_client.invoke_model(
            modelId="anthropic.claude-3-sonnet-20240229-v1:0",
            body=json.dumps({
                "prompt": user_message,
                "max_tokens_to_sample": 300
            })
        )
        bedrock_result = json.loads(response['body'].read())['completion']
    except Exception as e:
        bedrock_result = f"Bedrock error: {str(e)}"
    return f"Bedrock: {bedrock_result}"

# FastAPI route to invoke the agent
@fastapi_app.post("/invoke")
async def invoke_agent(payload: dict):
    return {"result": invoke(payload)}

# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8080)

