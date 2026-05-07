import uvicorn
from fastapi import FastAPI, Request
from bridge import TeamsMatrixBridge

app = FastAPI()

# Configuration (In production, use environment variables)
TEAMS_WEB_HOOK_URL = "http://localhost:8000/webhook"
MATRIX_HOMESERVER_URL = "https://matrix.org"
MATRIX_ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
MATRIX_USER_ID = "@bridge_user:matrix.org"
MATRIX_TARGET_ROOM = "!abc:matrix.org" 

bridge = TeamsMatrixBridge(
    teams_webhook_url=TEAMS_WEB_HOOK_URL,
    matrix_homeserver_url=MATRIX_HOMESERVER_URL,
    matrix_access_token=MATRIX_ACCESS_TOKEN,
    matrix_user_id=MATRIX_USER_ID
)

@app.post("/webhook")
async def teams_payload(request: Request):
    """Endpoint for Microsoft Teams incoming webhooks."""
    data = await request.json()
    if "room_id" not in data:
        data["room_id"] = MATRIX_TARGET_ROOM
        
    await bridge.handle_teams_event(data)
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
