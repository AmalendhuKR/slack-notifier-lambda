import json
import sys
import os

# Add the parent directory (where app.py is) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Now import the lambda_handler
from app import handler

# Load test event
event_file_path = os.path.join(os.path.dirname(__file__), "event.json")

# Load the test event JSON file
with open(event_file_path) as f:
    test_event = json.load(f)

# Simulate Lambda execution
response = handler(test_event, None)
print(response)
