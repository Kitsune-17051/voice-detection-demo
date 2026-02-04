# 🎙️ AI Voice Detection API - Setup Guide

## Quick Start (No ML Experience Required!)

This prototype API detects whether audio is AI-generated or human speech across 5 Indian languages.

---

## 📋 Prerequisites

You need to install Python. That's it!

### Install Python (if not already installed)

**Windows:**
1. Download from [python.org](https://www.python.org/downloads/)
2. Run installer and check "Add Python to PATH"

**Mac:**
```bash
brew install python
```

**Linux:**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

---

## 🚀 Installation Steps

### Step 1: Open Terminal/Command Prompt

**Windows:** Press `Win + R`, type `cmd`, press Enter  
**Mac/Linux:** Press `Cmd + Space`, type `terminal`, press Enter

### Step 2: Navigate to Project Folder

```bash
cd path/to/your/project/folder
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**If you get an error,** try:
```bash
pip3 install -r requirements.txt
```

---

## ▶️ Running the API

### Start the Server

```bash
python main.py
```

**If that doesn't work,** try:
```bash
python3 main.py
```

You should see:
```
🎙️  Starting AI Voice Detection API...
📍 Server running at: http://localhost:8000
📚 API Documentation: http://localhost:8000/docs
🔑 API Key: hackathon_2024_voice_detection_key
```

**✅ Success!** Your API is now running.

---

## 🧪 Testing the API

### Option 1: Automatic Test (Easiest)

Open a **NEW** terminal window (keep the server running in the first one):

```bash
python test_client.py
```

This will:
- Create a sample audio file
- Send it to your API
- Show the detection results

### Option 2: Interactive API Documentation

1. Keep the server running
2. Open browser and go to: `http://localhost:8000/docs`
3. You'll see an interactive interface where you can test the API

### Option 3: Using curl (Command Line)

```bash
# First, create a base64 encoded audio (or use existing)
curl -X POST "http://localhost:8000/api/v1/detect" \
  -H "X-API-Key: hackathon_2024_voice_detection_key" \
  -H "Content-Type: application/json" \
  -d '{
    "audio_base64": "YOUR_BASE64_AUDIO_HERE",
    "language": "english"
  }'
```

---

## 📡 API Usage

### Endpoint
```
POST http://localhost:8000/api/v1/detect
```

### Headers
```
X-API-Key: hackathon_2024_voice_detection_key
Content-Type: application/json
```

### Request Body
```json
{
  "audio_base64": "BASE64_ENCODED_MP3_AUDIO",
  "language": "english"
}
```

**Supported Languages:** `tamil`, `english`, `hindi`, `malayalam`, `telugu`

### Response
```json
{
  "classification": "AI_GENERATED",
  "confidence": 0.8734,
  "language": "english",
  "processing_time_ms": 12.45,
  "audio_duration_seconds": 3.2,
  "explanation": {
    "primary_indicators": [
      "Unnatural pitch consistency detected",
      "Spectral anomalies in high-frequency range"
    ],
    "language_specific_analysis": "English phonetic patterns analyzed",
    "confidence_factors": {
      "spectral_analysis": 0.892,
      "prosodic_features": 0.845,
      "artifact_detection": 0.923
    }
  }
}
```

---

## 🌐 Making API Public (For Submission)

To make your API accessible online for hackathon submission:

### Option 1: ngrok (Easiest, Free)

1. Download [ngrok](https://ngrok.com/download)
2. Run your API: `python main.py`
3. In new terminal: `ngrok http 8000`
4. Copy the public URL (e.g., `https://abc123.ngrok.io`)
5. Submit this URL to hackathon

### Option 2: Deploy to Cloud

**Render (Free):**
1. Create account at [render.com](https://render.com)
2. Connect your GitHub repo
3. Deploy as Web Service
4. Use free tier

**Railway (Free):**
1. Create account at [railway.app](https://railway.app)
2. Deploy from GitHub
3. Get public URL

---

## 🐛 Troubleshooting

### "Port already in use" error
```bash
# Kill process on port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F

# Mac/Linux:
lsof -ti:8000 | xargs kill -9
```

### "Module not found" error
```bash
pip install --upgrade -r requirements.txt
```

### API returns 401 error
Make sure you're using the correct API key in the header:
```
X-API-Key: hackathon_2024_voice_detection_key
```

---

## 📂 Project Structure

```
.
├── main.py              # Main API application
├── test_client.py       # Test script
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── sample_audio.mp3    # Auto-generated test file
```

---

## 🎯 For Hackathon Submission

Provide the following:

1. **API Endpoint:** `http://your-server-url:8000/api/v1/detect`
2. **API Key:** `hackathon_2024_voice_detection_key`
3. **Documentation:** Point to `/docs` endpoint or this README

---

## 💡 How It Works (High Level)

This prototype simulates AI voice detection using:

1. **Audio Validation:** Checks MP3 format and decodes Base64
2. **Mock Detection Algorithm:** 
   - Creates audio fingerprint using SHA-256 hash
   - Simulates feature extraction (spectral, prosodic analysis)
   - Returns classification with confidence score
3. **Explainability:** Provides reasons for classification

**For Production:** This would be replaced with:
- Real feature extraction (MFCCs, mel-spectrograms)
- ML models (Wav2Vec2, CNN ensemble)
- Actual acoustic analysis

---

## ⚡ Quick Commands Cheat Sheet

```bash
# Start API
python main.py

# Test API (new terminal)
python test_client.py

# View API docs in browser
http://localhost:8000/docs

# Check if server is running
curl http://localhost:8000/health

# Make API public with ngrok
ngrok http 8000
```

---

## 📞 Need Help?

- Check `/docs` endpoint for interactive API documentation
- Test with `test_client.py` first
- Make sure server is running before testing
- Verify API key is correct in all requests

---

**Good luck with your hackathon! 🚀**
