#!/usr/bin/env python3

import boto3
import json
import uuid

client = boto3.client("bedrock-agentcore", region_name="us-west-2")

input_text = "Hello, how can you assist me today?"
session_id = f"session-{uuid.uuid4().hex}"

response = client.invoke_agent_runtime(
    agentRuntimeArn="arn:aws:bedrock-agentcore:us-west-2:513826297540:runtime/shahzad_open_research_agent-Z1Nkzj8CRs",
    qualifier="DEFAULT",
    runtimeSessionId=session_id,
    payload=json.dumps({"input": input_text}).encode("utf-8")
)

# Read from the StreamingBody
for line in response["response"].iter_lines():
    if line:
        print(line.decode("utf-8"))

