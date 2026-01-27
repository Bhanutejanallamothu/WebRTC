import json

broadcaster = None
listeners = set()

async def signaling_handler(websocket):
    global broadcaster

    try:
        async for message in websocket:
            data = json.loads(message)

            role = data.get("role")
            msg_type = data.get("type")

            # Register broadcaster
            if role == "broadcaster":
                broadcaster = websocket
                print("🎙️ Broadcaster connected")

            # Register listener
            elif role == "listener":
                listeners.add(websocket)
                print("🎧 Listener connected")

            # Broadcaster sends offer → listeners
            if websocket == broadcaster and msg_type == "offer":
                for listener in listeners:
                    await listener.send(json.dumps(data))

            # Listener sends answer → broadcaster
            elif websocket in listeners and msg_type == "answer":
                if broadcaster:
                    await broadcaster.send(json.dumps(data))

            # ICE candidates (both directions)
            elif msg_type == "ice-candidate":
                if websocket == broadcaster:
                    for listener in listeners:
                        await listener.send(json.dumps(data))
                elif websocket in listeners and broadcaster:
                    await broadcaster.send(json.dumps(data))

    except Exception as e:
        print("Connection error:", e)

    finally:
        listeners.discard(websocket)
        if websocket == broadcaster:
            broadcaster = None
            print("🎙️ Broadcaster disconnected")
