from strands import Agent, tool
from strands.models import BedrockModel
import argparse
import json
from bedrock_agentcore.runtime import BedrockAgentCoreApp

app = BedrockAgentCoreApp()

@tool
def get_return_policy(product_category: str) -> str:
    """Get return policy for a specific product category."""
    policies = {
        "electronics": "30-day return policy for electronics. Items must be in original packaging with all accessories. Restocking fee may apply.",
        "clothing": "60-day return policy for clothing. Items must have tags attached and be unworn.",
        "books": "Returns accepted within 30 days if in good condition.",
        "home": "45-day return policy for home goods. Large items may require special shipping.",
        "beauty": "30-day return policy for beauty products. Must be unopened for hygiene reasons."
    }
    
    policy = policies.get(product_category.lower())
    if policy:
        return f"Return Policy for {product_category.title()}: {policy}"
    else:
        return f"Standard 30-day return policy applies to {product_category}. Items must be in original condition."
 
## Important
#### 
# Copy other tools here
####

model_id = "amazon.titan-text-express-v1"
# model_id = "us.anthropic.claude-sonnet-4-20250514-v1:0"
model = BedrockModel(model_id=model_id)

agent = Agent(
    model=model,
#   tools=[get_return_policy, <Insert other tool names here>],
    system_prompt="""You are a helpful and professional customer support assistant for an e-commerce company.
        
        Your role is to assist customers with:
        - Order status inquiries
        - Product information requests  
        - Shipping and delivery questions
        - Return and refund policy questions
        
        Guidelines for interactions:
        - Always be polite, professional, and empathetic
        - Use the available tools to provide accurate, up-to-date information
        - If you cannot find specific information, acknowledge this and offer alternatives
        - Keep responses clear and concise while being thorough
        - If a customer has a complex issue that requires human intervention, politely suggest they contact our support team
        
        Remember: Your goal is to provide excellent customer service and resolve customer inquiries efficiently."""
)

@app.entrypoint
def customer_support_agent(payload):
    """
    Invoke the agent with a payload
    """
    user_input = payload.get("prompt")
    print("User input:", user_input)
    response = agent(user_input)
    return response.message['content'][0]['text']

if __name__ == "__main__":
    app.run()

