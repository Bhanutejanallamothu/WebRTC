import asyncio
import websockets
from signaling_api import signaling_handler

async def main():
    async with websockets.serve(
        signaling_handler,
        "0.0.0.0",
        8765
    ):
        print("✅ Signaling API running on ws://localhost:8765")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
