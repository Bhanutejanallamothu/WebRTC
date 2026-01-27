import asyncio
import json
import sounddevice as sd
import numpy as np
import av
import fractions
import websockets
from aiortc import RTCPeerConnection, RTCSessionDescription, MediaStreamTrack

SIGNALING_URL = "ws://localhost:8000/ws"
SAMPLE_RATE = 48000
DEVICE_INDEX = 4   # change if needed

audio_queue = asyncio.Queue()

def audio_callback(indata, frames, time, status):
    pcm = (indata[:, 0] * 32767).astype(np.int16)
    asyncio.get_event_loop().call_soon_threadsafe(
        audio_queue.put_nowait, pcm
    )

class AudioTrack(MediaStreamTrack):
    kind = "audio"

    async def recv(self):
        pcm = await audio_queue.get()
        frame = av.AudioFrame.from_ndarray(pcm, layout="mono")
        frame.sample_rate = SAMPLE_RATE
        frame.time_base = fractions.Fraction(1, SAMPLE_RATE)
        return frame

async def run_sender():
    peers = {}
    audio_track = AudioTrack()

    stream = sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        device=DEVICE_INDEX,
        callback=audio_callback
    )
    stream.start()

    async with websockets.connect(SIGNALING_URL) as ws:
        await ws.send("sender")
        print("Sender registered")

        while True:
            msg = json.loads(await ws.recv())
            peer_id = msg["from"]

            if msg["type"] == "listener":
                pc = RTCPeerConnection()
                pc.addTrack(audio_track)
                peers[peer_id] = pc

                offer = await pc.createOffer()
                await pc.setLocalDescription(offer)

                await ws.send(json.dumps({
                    "type": "offer",
                    "sdp": offer.sdp,
                    "target": peer_id
                }))

            elif msg["type"] == "answer":
                await peers[peer_id].setRemoteDescription(
                    RTCSessionDescription(msg["sdp"], "answer")
                )

if __name__ == "__main__":
    asyncio.run(run_sender())
