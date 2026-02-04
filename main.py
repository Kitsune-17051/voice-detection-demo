"""
AI Voice Detection API - Prototype
Detects AI-generated voices across Tamil, English, Hindi, Malayalam, Telugu
"""

import os
import base64
import hashlib
import random
from datetime import datetime
from typing import Literal

from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field


app = FastAPI(
    title="AI Voice Detection API",
    description="Detects whether audio is AI-generated or human speech",
    version="1.0.0"
)

# 🔐 Load API key from environment variable
VALID_API_KEY = os.getenv("VOICE_API_KEY")

if not VALID_API_KEY:
    raise RuntimeError("❌ VOICE_API_KEY environment variable is not set!")


SUPPORTED_LANGUAGES = ["tamil", "english", "hindi", "malayalam", "telugu"]


class AudioRequest(BaseModel):
    audio_base64: str = Field(..., description="Base64 encoded MP3 audio file")
    language: Literal["tamil", "english", "hindi", "malayalam", "telugu"] = "english"


class DetectionResponse(BaseModel):
    classification: Literal["AI_GENERATED", "HUMAN"]
    confidence: float = Field(..., ge=0.0, le=1.0)
    language: str
    processing_time_ms: float
    audio_duration_seconds: float
    explanation: dict


def verify_api_key(api_key: str):
    if api_key != VALID_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")


def decode_audio(audio_base64: str):
    try:
        audio_bytes = base64.b64decode(audio_base64)

        if not audio_bytes.startswith(b'\xff\xfb') and not audio_bytes.startswith(b'ID3'):
            raise ValueError("Invalid MP3 format")

        file_size_kb = len(audio_bytes) / 1024
        estimated_duration = file_size_kb / 16

        return audio_bytes, estimated_duration
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid audio data: {str(e)}")


def mock_ai_detection(audio_bytes: bytes, language: str):
    audio_hash = hashlib.sha256(audio_bytes).hexdigest()
    hash_value = int(audio_hash[:16], 16)
    random.seed(hash_value)

    is_ai = random.random() < 0.6
    classification = "AI_GENERATED" if is_ai else "HUMAN"

    confidence = (
        0.75 + random.random() * 0.23 if is_ai
        else 0.70 + random.random() * 0.25
    )

    indicators = [
        "Unnatural pitch consistency detected",
        "Spectral anomalies in high-frequency range",
        "Irregular breathing pattern intervals",
        "Phase coherence artifacts present",
        "Prosody smoothness exceeds human baseline"
    ] if is_ai else [
        "Natural voice tremor patterns detected",
        "Organic breathing sounds present",
        "Micro-variations in pitch consistent with human speech",
        "Formant transitions show natural articulatory movement",
        "Background noise characteristics indicate real recording"
    ]

    explanation = {
        "primary_indicators": random.sample(indicators, k=3),
        "language_specific_analysis": f"{language.capitalize()} phonetic patterns analyzed",
        "confidence_factors": {
            "spectral_analysis": round(random.uniform(0.7, 0.95), 3),
            "prosodic_features": round(random.uniform(0.65, 0.92), 3),
            "artifact_detection": round(random.uniform(0.70, 0.98), 3)
        }
    }

    return classification, round(confidence, 4), explanation


@app.post("/api/v1/detect", response_model=DetectionResponse)
async def detect_voice(
    request: AudioRequest,
    api_key: str = Header(..., alias="X-API-Key")
):
    start_time = datetime.utcnow()

    verify_api_key(api_key)

    if request.language not in SUPPORTED_LANGUAGES:
        raise HTTPException(status_code=400, detail="Unsupported language")

    audio_bytes, duration = decode_audio(request.audio_base64)
    classification, confidence, explanation = mock_ai_detection(audio_bytes, request.language)

    processing_time = (datetime.utcnow() - start_time).total_seconds() * 1000

    return DetectionResponse(
        classification=classification,
        confidence=confidence,
        language=request.language,
        processing_time_ms=round(processing_time, 2),
        audio_duration_seconds=round(duration, 2),
        explanation=explanation
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.utcnow().isoformat()
        }
    )


if __name__ == "__main__":
    import uvicorn
    print("🎙️  Starting AI Voice Detection API...")
    print("📍 Server running at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
