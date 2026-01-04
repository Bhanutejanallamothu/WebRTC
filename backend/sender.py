import asyncio
import json
import sounddevice as sd
import numpy as np
import av
import fractions
import websockets
from aiortc import RTCPeerConnection, RTCSessionDescription, MediaStreamTrack

SIGNALING_URL = "ws://localhost:8000/ws/sender"

ICE = [
    {"urls": "stun:stun.l.google.com:19302"}
]

class AudioTrack(MediaStreamTrack):
    kind = "audio"

    def __init__(self):
        super().__init__()
        self.queue = asyncio.Queue()
        self.rate = 48000

        def callback(indata, frames, time, status):
            pcm = (indata[:, 0] * 32767).astype(np.int16)
            asyncio.get_event_loop().call_soon_threadsafe(
                self.queue.put_nowait, pcm
            )

        self.stream = sd.InputStream(
            samplerate=self.rate,
            channels=1,
            dtype="float32",
            device=4,
            callback=callback
        )
        self.stream.start()

    async def recv(self):
        pcm = await self.queue.get()
        print("Audio frame:", pcm[:5])
        frame = av.AudioFrame.from_ndarray(pcm, layout="mono")
        frame.sample_rate = self.rate
        frame.time_base = fractions.Fraction(1, self.rate)
        return frame


async def run_sender():
    peers = {}

    while True:
        try:
            print("Connecting to signaling server...")
            async with websockets.connect(SIGNALING_URL) as ws:
                print("Connected to signaling")

                while True:
                    msg = json.loads(await ws.recv())
                    sender = msg.get("from")

                    if msg["type"] == "answer":
                        await peers[sender].setRemoteDescription(
                            RTCSessionDescription(msg["sdp"], "answer")
                        )

                    elif msg["type"] == "candidate":
                        await peers[sender].addIceCandidate(msg["candidate"])

                    elif msg["type"] == "listener":
                        if sender not in peers:
                            print("New listener:", sender)
                            pc = RTCPeerConnection({"iceServers": ICE})
                            pc.addTrack(AudioTrack())
                            peers[sender] = pc

                            offer = await pc.createOffer()
                            await pc.setLocalDescription(offer)

                            await ws.send(json.dumps({
                                "type": "offer",
                                "sdp": offer.sdp,
                                "target": sender,
                                "from": "sender"
                            }))

        except asyncio.CancelledError:
            print("Sender cancelled, shutting down")
            break

        except Exception as e:
            print("Connection lost, retrying in 2s:", e)
            await asyncio.sleep(2)


if __name__ == "__main__":
    try:
        asyncio.run(run_sender())
    except KeyboardInterrupt:
        print("Sender stopped by user")
