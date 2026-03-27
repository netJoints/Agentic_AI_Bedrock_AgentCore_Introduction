import json
import urllib3
import boto3
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info("=== USING DIRECT HTTP TO AGENTCORE ===")
    logger.info(f"Received event: {json.dumps(event)}")
    
    try:
        # Extract prompt
        prompt = event.get('prompt', 'Hello from travel supervisor')
        logger.info(f"Extracted prompt: {prompt}")
        
        # AgentCore agents use direct HTTP endpoints
        # Based on your agent ARN, construct the endpoint
        agent_endpoint = "https://shahzad_ai_agent1-7xlgUJCNlk.runtime.bedrock-agentcore.us-west-2.amazonaws.com"
        
        # Create HTTP client
        http = urllib3.PoolManager()
        
        # Prepare request data
        request_data = {
            "prompt": prompt
        }
        
        # Get AWS credentials for authentication
        session = boto3.Session()
        credentials = session.get_credentials()
        
        # Make request to AgentCore endpoint
        response = http.request(
            'POST',
            f"{agent_endpoint}/invoke",
            body=json.dumps(request_data),
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'AWS4-HMAC-SHA256 Credential={credentials.access_key}'
            }
        )
        
        if response.status == 200:
            response_data = json.loads(response.data.decode('utf-8'))
            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'success': True,
                    'version': 'DIRECT_HTTP_TO_AGENTCORE',
                    'agent_response': response_data
                })
            }
        else:
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'error': f'HTTP {response.status}: {response.data.decode("utf-8")}'
                })
            }
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
