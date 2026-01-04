from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json

app = FastAPI()
clients = {}

@app.websocket("/ws/{client_id}")
async def ws(websocket: WebSocket, client_id: str):
    await websocket.accept()
    clients[client_id] = websocket
    print(f"Client connected: {client_id}")

    try:
        while True:
            message = await websocket.receive_text()
            data = json.loads(message)

            msg_type = data.get("type")

            if msg_type == "listener":
                print(f"Listener announced: {data.get('from')}")
                sender_ws = clients.get("sender")
                if sender_ws:
                    await sender_ws.send_text(message)
                continue

            target = data.get("target")
            if target and target in clients:
                await clients[target].send_text(message)

    except WebSocketDisconnect:
        print(f"Client disconnected: {client_id}")
        clients.pop(client_id, None)
