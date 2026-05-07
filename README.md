# Teams to Matrix Bridge
This bot acts as a bridge that receives messages from Microsoft Teams (via Webhooks) and posts them into a Matrix room.

## How it works
1. Microsoft Teams sends a JSON payload to the `/webhook` endpoint.
2. The bridge parses the message and sends it to the configured Matrix room using the Matrix Client-Server API.

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Configure `main.py` with your Matrix credentials.
3. Run the server: `python main.py`
