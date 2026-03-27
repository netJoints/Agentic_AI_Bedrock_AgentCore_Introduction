#!/usr/bin/env python3
import boto3
import json
import uuid
import re

client = boto3.client("bedrock-agentcore", region_name="us-west-2")
session_id = f"session-{uuid.uuid4().hex}"

print(f"Session ID: {session_id}")
print("Connected to shahzad_open_research_agent")
print("\n⚠️  This is a RESEARCH agent - it expects detailed research queries!")
print("Try prompts like:")
print("  - 'Write a report on the latest developments in quantum computing'")
print("  - 'Research the impact of AI on healthcare in 2024'")
print("  - 'Analyze the current state of renewable energy technologies'")
print("\nType 'exit' or press CTRL+C to quit\n")

def clean_response(text):
    """Clean up the response text"""
    # Remove escaped quotes and newlines
    text = text.strip('"\\')
    text = text.replace('\\n', '\n')
    text = text.replace('\\"', '"')
    text = text.replace("\\'", "'")
    
    # Extract content from AIMessage if present
    if 'AIMessage' in text and 'content=' in text:
        match = re.search(r"content=['\"]([^'\"]+)['\"]", text)
        if match:
            return match.group(1).replace('\\n', '\n')
    
    # Remove data: prefix if present
    if text.startswith('data: '):
        text = text[6:]
    
    return text

try:
    while True:
        input_text = input("\nYou: ")
        
        if input_text.lower() in ['exit', 'quit']:
            break
            
        if not input_text.strip():
            continue
        
        # For the research agent, let's be more explicit
        if len(input_text.split()) < 5:  # If query is too short
            print("\n💡 Tip: This agent works better with detailed queries. Try something like:")
            print("   'Research and write a report about [your topic] including [specific aspects]'")
        
        response = client.invoke_agent_runtime(
            agentRuntimeArn="arn:aws:bedrock-agentcore:us-west-2:513826297540:runtime/shahzad_open_research_agent-Z1Nkzj8CRs",
            qualifier="DEFAULT",
            runtimeSessionId=session_id,
            payload=json.dumps({"input": input_text}).encode("utf-8")
        )
        
        print("\nAgent: ", end="")
        
        # Collect all response lines
        full_response = []
        for line in response["response"].iter_lines():
            if line:
                decoded = line.decode("utf-8")
                full_response.append(decoded)
        
        # Process and display the response
        complete_text = "".join(full_response)
        cleaned = clean_response(complete_text)
        
        # If response seems truncated, show what we got
        if cleaned.endswith("To get started"):
            print(cleaned + "... [Response truncated - try a more specific query]")
        else:
            print(cleaned)
        
except KeyboardInterrupt:
    print("\n\nGoodbye!")
except Exception as e:
    print(f"\nError: {e}")
