import json
import sys
import os

# Add the parent directory (where app.py is) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import the Lambda handler
from app import handler

# Define path to test event JSON file
event_file_path = os.path.join(os.path.dirname(__file__), "event.json")

# Load the test event JSON content
with open(event_file_path, "r") as f:
    event_payload = json.load(f)

# Simulate an API Gateway event format
test_event = {
    "body": json.dumps(event_payload)
}

# Run the handler with the test event
response = handler(test_event, None)

# Print the Lambda response
print(json.dumps(response, indent=2))
