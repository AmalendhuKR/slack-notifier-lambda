import json
import os
import urllib3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def handler(event, context):
    # Get the Slack Webhook URL from environment variables
    slack_webhook_url = os.getenv('SLACK_WEBHOOK_URL')

    if not slack_webhook_url:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Missing SLACK_WEBHOOK_URL"})
        }

    http = urllib3.PoolManager()

    # Extract message from API Gateway event body
    try:
        body = json.loads(event['body'])
        message = body.get('message', '')
    except (json.JSONDecodeError, TypeError):
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid JSON body"})
        }

    if not message:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing 'message' field in request body"})
        }

    # Send message to Slack
    msg = {"text": message}
    encoded_msg = json.dumps(msg).encode('utf-8')
    response = http.request('POST', slack_webhook_url, body=encoded_msg)

    return {
        "statusCode": response.status,
        "body": json.dumps({"message": "Notification sent to Slack"})
    }
