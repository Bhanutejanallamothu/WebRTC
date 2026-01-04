import React, { useEffect } from "react"

export default function App() {
  useEffect(() => {
    const id = "listener-" + Math.random().toString(36).slice(2)

    const pc = new RTCPeerConnection({
      iceServers: [{ urls: "stun:stun.l.google.com:19302" }]
    })

    const ws = new WebSocket("ws://localhost:8000/ws/" + id)

    let audioEl = null

    ws.onopen = () => {
      ws.send(JSON.stringify({
        type: "listener",
        from: id
      }))
    }

    pc.ontrack = e => {
      if (!audioEl) {
        audioEl = document.createElement("audio")
        audioEl.srcObject = e.streams[0]
        audioEl.autoplay = true
        audioEl.muted = false
        audioEl.play().catch(console.error)
        document.body.appendChild(audioEl)
      }
    }

    pc.onicecandidate = e => {
      if (e.candidate && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({
          type: "candidate",
          candidate: e.candidate,
          target: "sender",
          from: id
        }))
      }
    }

    ws.onmessage = async e => {
      const msg = JSON.parse(e.data)

      if (msg.type === "offer") {
        await pc.setRemoteDescription(msg)
        const answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)

        ws.send(JSON.stringify({
          type: "answer",
          sdp: answer.sdp,
          target: "sender",
          from: id
        }))
      }
    }

    return () => {
      ws.close()
      pc.close()
      if (audioEl) audioEl.remove()
    }
  }, [])

  return <h2>Live Audio Stream</h2>
}
