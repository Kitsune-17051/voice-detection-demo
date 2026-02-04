"""
AI Voice Detection API - Prototype
Detects AI-generated voices across Tamil, English, Hindi, Malayalam, Telugu
"""



from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import base64
import io
import hashlib
import random
from datetime import datetime
from typing import Literal

app = FastAPI(
    title="AI Voice Detection API",
    description="Detects whether audio is AI-generated or human speech",
    version="1.0.0"
)

# API Key for authentication (change this for production)
VALID_API_KEY = "hackathon_2024_voice_detection_key"

# Supported languages
SUPPORTED_LANGUAGES = ["tamil", "english", "hindi", "malayalam", "telugu"]

class AudioRequest(BaseModel):
    audio_base64: str = Field(..., description="Base64 encoded MP3 audio file")
    language: Literal["tamil", "english", "hindi", "malayalam", "telugu"] = Field(
        default="english",
        description="Expected language of the audio"
    )

class DetectionResponse(BaseModel):
    classification: Literal["AI_GENERATED", "HUMAN"]
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score between 0.0 and 1.0")
    language: str
    processing_time_ms: float
    audio_duration_seconds: float
    explanation: dict

def verify_api_key(api_key: str):
    """Verify the API key"""
    if api_key != VALID_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

def decode_audio(audio_base64: str):
    """Decode base64 audio and perform basic validation"""
    try:
        audio_bytes = base64.b64decode(audio_base64)
        
        # Check if it's a valid MP3 (basic check for MP3 header)
        if not audio_bytes.startswith(b'\xff\xfb') and not audio_bytes.startswith(b'ID3'):
            raise ValueError("Invalid MP3 format")
        
        # Estimate duration (rough approximation)
        file_size_kb = len(audio_bytes) / 1024
        estimated_duration = file_size_kb / 16  # Assume ~16KB per second for MP3
        
        return audio_bytes, estimated_duration
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid audio data: {str(e)}")

def mock_ai_detection(audio_bytes: bytes, language: str):
    """
    Mock AI detection algorithm that simulates realistic detection
    
    In production, this would be replaced with:
    - Feature extraction (MFCCs, spectrograms, prosody)
    - ML model inference (Wav2Vec2, CNN ensemble)
    - Confidence calculation
    """
    
    # Create a deterministic "fingerprint" from audio
    audio_hash = hashlib.sha256(audio_bytes).hexdigest()
    hash_value = int(audio_hash[:16], 16)
    
    # Use hash to create consistent but seemingly random results
    random.seed(hash_value)
    
    # Simulate detection with realistic distribution
    # 60% chance of detecting AI, 40% human (adjustable)
    is_ai = random.random() < 0.6
    
    classification = "AI_GENERATED" if is_ai else "HUMAN"
    
    # Generate confidence score (higher for clear cases)
    if is_ai:
        # AI detection confidence: 0.75 to 0.98
        confidence = 0.75 + random.random() * 0.23
    else:
        # Human detection confidence: 0.70 to 0.95
        confidence = 0.70 + random.random() * 0.25
    
    # Generate mock feature explanations
    features_detected = []
    
    if is_ai:
        ai_indicators = [
            "Unnatural pitch consistency detected",
            "Spectral anomalies in high-frequency range",
            "Irregular breathing pattern intervals",
            "Phase coherence artifacts present",
            "Prosody smoothness exceeds human baseline"
        ]
        # Select 2-3 random indicators
        features_detected = random.sample(ai_indicators, k=random.randint(2, 3))
    else:
        human_indicators = [
            "Natural voice tremor patterns detected",
            "Organic breathing sounds present",
            "Micro-variations in pitch consistent with human speech",
            "Formant transitions show natural articulatory movement",
            "Background noise characteristics indicate real recording"
        ]
        features_detected = random.sample(human_indicators, k=random.randint(2, 3))
    
    explanation = {
        "primary_indicators": features_detected,
        "language_specific_analysis": f"{language.capitalize()} phonetic patterns analyzed",
        "confidence_factors": {
            "spectral_analysis": round(random.uniform(0.7, 0.95), 3),
            "prosodic_features": round(random.uniform(0.65, 0.92), 3),
            "artifact_detection": round(random.uniform(0.70, 0.98), 3)
        }
    }
    
    return classification, round(confidence, 4), explanation

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "AI Voice Detection API",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "detect": "/api/v1/detect",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "supported_languages": SUPPORTED_LANGUAGES
    }

@app.post("/api/v1/detect", response_model=DetectionResponse)
async def detect_voice(
    request: AudioRequest,
    api_key: str = Header(..., alias="X-API-Key")
):
    """
    Detect if audio is AI-generated or human speech
    
    Parameters:
    - audio_base64: Base64 encoded MP3 audio file
    - language: Expected language (tamil, english, hindi, malayalam, telugu)
    
    Returns:
    - classification: AI_GENERATED or HUMAN
    - confidence: Confidence score (0.0 to 1.0)
    - explanation: Detailed analysis of detection
    """
    
    start_time = datetime.utcnow()
    
    # Verify API key
    verify_api_key(api_key)
    
    # Validate language
    if request.language.lower() not in SUPPORTED_LANGUAGES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported language. Supported: {', '.join(SUPPORTED_LANGUAGES)}"
        )
    
    # Decode and validate audio
    audio_bytes, duration = decode_audio(request.audio_base64)
    
    # Perform AI detection (mock for prototype)
    classification, confidence, explanation = mock_ai_detection(
        audio_bytes,
        request.language
    )
    
    # Calculate processing time
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
    """Custom error handler"""
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
    print(f"🔑 API Key: {VALID_API_KEY}")
    uvicorn.run(app, host="0.0.0.0", port=8000)
