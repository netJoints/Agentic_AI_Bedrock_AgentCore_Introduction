from strands import Agent, tool
from strands_tools import calculator
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from strands.models import BedrockModel
from fastapi import FastAPI

# Initialize FastAPI and AgentCore
fastapi_app = FastAPI()
agentcore_app = BedrockAgentCoreApp()

# Health check endpoint required by AgentCore
@fastapi_app.get("/health")
async def health():
    return {"status": "ok"}

from fastapi import Request
from pydantic import BaseModel

class Prompt(BaseModel):
    prompt: str

@fastapi_app.post("/invoke")
async def invoke(prompt: Prompt):
    payload = {"prompt": prompt.prompt}
    result = strands_agent_bedrock(payload)
    return {"response": result}

# Define a custom tool
@tool
def weather():
    """Get weather"""
    return "It's sunny in Tokyo today."

# Configure Bedrock model
model_id = "anthropic.claude-instant-v1"
model = BedrockModel(model_id=model_id)

# Create the agent with tools
agent = Agent(
    model=model,
    tools=[calculator, weather],
    system_prompt="You're a helpful assistant. You can do simple math calculations and tell the weather."
)

# AgentCore entrypoint
@agentcore_app.entrypoint
def strands_agent_bedrock(payload):
    user_input = payload.get("prompt", "Hello")
    print("User input:", user_input)
    response = agent(user_input)
    
    # Inspect the structure of the response
    print("Agent response:", response.message)
    
    # Safely extract the text
    try:
        # If response.message is a dict with 'content' as a list of dicts
        content = response.message.get("content", [])
        if isinstance(content, list) and len(content) > 0:
            first_item = content[0]
            if isinstance(first_item, dict) and "text" in first_item:
                return first_item["text"]
        return "Unexpected response format."
    except Exception as e:
        print("Error extracting response:", e)
        return f"Error: {str(e)}"

# Mount AgentCore app into FastAPI
fastapi_app.mount("/", agentcore_app)

# Run the FastAPI app
if __name__ == "__main__":    
    import uvicorn
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8080)
