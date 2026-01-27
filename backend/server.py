import asyncio
import os
import websockets
from signaling_api import signaling_handler

async def main():
    port = int(os.environ.get("PORT", 8765))
    async with websockets.serve(
        signaling_handler,
        "0.0.0.0",
        port
    ):
        print(f"Signaling API running on ws://0.0.0.0:{port}")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
