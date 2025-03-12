import json
import os
import urllib3
from dotenv import load_dotenv

# Load environment variables (useful for local testing)
load_dotenv()

http = urllib3.PoolManager()

def handler(event, context):
    # Helper to format the response correctly
    def response(status_code, body_dict):
        return {
            "statusCode": status_code,
            "body": json.dumps(body_dict)
        }

    # Get the Slack Webhook URL from environment variables
    slack_webhook_url = os.getenv('SLACK_WEBHOOK_URL')

    if not slack_webhook_url:
        return response(500, {"error": "Missing SLACK_WEBHOOK_URL"})

    # Extract and validate JSON body from API Gateway event
    if 'body' not in event or not event['body']:
        return response(400, {"error": "Missing request body"})

    try:
        body = json.loads(event['body'])
    except (json.JSONDecodeError, TypeError):
        return response(400, {"error": "Invalid JSON in request body"})
    
    # Empty JSON body
    if not isinstance(body, dict) or not body:
        return response(400, {"error": "Empty JSON body is not allowed"})

    # Format the full JSON payload into a string
    try:
        message_text = json.dumps(body, indent=2)
    except Exception as e:
        return response(500, {"error": f"Failed to format message: {str(e)}"})

    # Send the message to Slack
    msg = {"text": f"*Data:*\n```{message_text}```"}
    encoded_msg = json.dumps(msg).encode('utf-8')

    try:
        slack_response = http.request(
            'POST',
            slack_webhook_url,
            body=encoded_msg,
            headers={"Content-Type": "application/json"}
        )
    except Exception as e:
        return response(500, {"error": f"Failed to send message to Slack: {str(e)}"})

    return response(slack_response.status, {"message": "Notification sent to Slack"})
