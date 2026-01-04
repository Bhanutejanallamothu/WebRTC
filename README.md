# 🎧 WebRTC Live Audio Streaming (Python + React)

This project implements **real-time live audio streaming** from a **USB / AUX / Line-In audio source** on a sender machine to **multiple browser listeners** using **WebRTC**.

The backend is built with **Python (FastAPI + aiortc)** and the frontend is built with **React (Vite)**.  
Audio is captured using **sounddevice** and transmitted with **low latency** via WebRTC.

---

## ✨ Features

- 🎙️ Capture live audio from USB / AUX / Line-In
- 🌐 Stream audio to browsers using WebRTC
- 👥 Support multiple listeners
- 🔁 Auto-reconnect for sender
- ⚡ Low-latency real-time audio
- 🧠 Simple WebSocket signaling (FastAPI)
- 🖥️ React frontend (no plugins required)

---

## 🏗️ Architecture Overview

```

Audio Input (USB / AUX)
↓
Python Sender (aiortc + sounddevice)
↓
WebSocket Signaling (FastAPI)
↓
WebRTC
↓
React Browser Listeners

```

---

## 📁 Project Structure

```

webrtc-audio-app/
├── backend/
│   ├── sender.py          # Audio capture + WebRTC sender
│   └── signaling.py       # WebSocket signaling server
│
├── frontend/
│   └── react-app/
│       ├── index.html
│       ├── package.json
│       └── src/
│           ├── main.jsx
│           └── App.jsx
│
├── requirements.txt
└── README.md

````

---

## 🛠️ Requirements

### Backend
- Python **3.11.x** (recommended)
- Windows / Linux / macOS
- USB mic, Line-In, or AUX audio source

### Frontend
- Node.js 18+
- Modern browser (Chrome / Edge / Firefox)

---

## ⚙️ Backend Setup

### 1️⃣ Create virtual environment

```bash
python -m venv venv
````

Activate it:

**Windows**

```powershell
venv\Scripts\Activate.ps1
```

**Linux / macOS**

```bash
source venv/bin/activate
```

---

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Start signaling server

```bash
uvicorn backend.signaling:app --host localhost --port 8000
```

Keep this terminal running.

---

### 4️⃣ Start the audio sender

> ⚠️ Make sure a browser listener is open before starting the sender.

```bash
python backend/sender.py
```

---

## 🌐 Frontend Setup

```bash
cd frontend/react-app
npm install
npm run dev
```

Open the browser at:

```
http://localhost:5173
```

---

## 🔊 Selecting Audio Input Device (Important)

List available audio devices:

```bash
python - << EOF
import sounddevice as sd
print(sd.query_devices())
EOF
```

Update `device=` in `backend/sender.py`:

```python
sd.InputStream(
    samplerate=48000,
    channels=1,
    device=DEVICE_INDEX,
    callback=callback
)
```

---

## ▶️ Correct Run Order (Very Important)

1. **Start signaling server**
2. **Open React app in browser**
3. **Start Python sender**

If the order is wrong, audio will not start.

---

## 🧪 Testing Checklist

* Sender console shows: `New listener`
* Browser creates `<audio>` element
* Audio is audible with slight latency
* Multiple tabs receive audio simultaneously

---

## 🚀 Future Improvements

* TURN server support (internet streaming)
* Volume / mute controls
* Stream rooms
* Authentication
* Recording
* Deployment (Docker / Cloud)

---

## ⚠️ Notes

* Python **3.14 is NOT supported** (use 3.11)
* React StrictMode is disabled for WebRTC stability
* Chrome may block autoplay → allow sound manually

---

## 📜 License

MIT License

---

## 🤝 Contribution

Pull requests are welcome.
This project is designed to be **simple, educational, and extensible**.

---



Just tell me 👍
```
