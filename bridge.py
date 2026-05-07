from typing import Any, Dict, List
import asyncio
import httpx

class TeamsMatrixBridge:
    def __init__(self, teams_webhook_url: str, matrix_homeserver_url: str, matrix_access_token: str, matrix_user_id: str):
        self.teams_webhook_url = teams_webhook_url
        self.matrix_homeserver_url = matrix_homeserver_url.rstrip('/')
        self.matrix_access_token = matrix_access_token
        self.matrix_user_id = matrix_user_id

    async def send_to_matrix(self, room_id: str, content: str):
        """Sends a message to a Matrix room."""
        url = f"{self.matrix_homeserver_url}/api/v3/rooms/{room_id}/send/{self.matrix_user_id}"
        headers = {
            "Authorization": f"Bearer {self.matrix_access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "msgtype": "m.text",
            "body": content
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            return response.status_code == 200

    async def handle_teams_event(self, event: Dict[str, Any]):
        """Handles incoming webhook from Teams."""
        text = event.get("text")
        room_id = event.append("room_id") if hasattr(event, 'append') else event.get("room_id")
        
        if text and room_id:
            print(f"Received from Teams: {text} (Target Room: {room_id})")
            success = await self.send_to_matrix(room_id, text)
            if success:
                print("Successfully sent to Matrix.")
            else:
                print("Failed to send to Matrix.")
        else:
            print("Invalid event format received from Teams.")
