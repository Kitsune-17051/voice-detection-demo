"""
Test Client for AI Voice Detection API
Demonstrates how to call the API with sample audio
"""

import requests
import base64
import json
from pathlib import Path

# API Configuration
API_URL = "http://localhost:8000/api/v1/detect"
API_KEY = "hackathon_2024_voice_detection_key"

def encode_audio_file(file_path):
    """Read and encode audio file to base64"""
    with open(file_path, 'rb') as audio_file:
        audio_bytes = audio_file.read()
        encoded = base64.b64encode(audio_bytes).decode('utf-8')
    return encoded

def test_detection(audio_path, language="english"):
    """
    Test the voice detection API
    
    Args:
        audio_path: Path to MP3 audio file
        language: Language of the audio (tamil, english, hindi, malayalam, telugu)
    """
    
    print(f"\n{'='*60}")
    print(f"Testing: {audio_path}")
    print(f"Language: {language}")
    print(f"{'='*60}\n")
    
    try:
        # Encode audio
        print("📦 Encoding audio to Base64...")
        audio_base64 = encode_audio_file(audio_path)
        print(f"✅ Audio encoded ({len(audio_base64)} characters)")
        
        # Prepare request
        payload = {
            "audio_base64": audio_base64,
            "language": language
        }
        
        headers = {
            "X-API-Key": API_KEY,
            "Content-Type": "application/json"
        }
        
        # Make API call
        print("\n🔍 Calling detection API...")
        response = requests.post(API_URL, json=payload, headers=headers)
        
        # Handle response
        if response.status_code == 200:
            result = response.json()
            print("\n✅ Detection Successful!\n")
            print(f"Classification: {result['classification']}")
            print(f"Confidence: {result['confidence']:.2%}")
            print(f"Language: {result['language']}")
            print(f"Processing Time: {result['processing_time_ms']:.2f}ms")
            print(f"Audio Duration: {result['audio_duration_seconds']:.2f}s")
            print(f"\n📊 Analysis:")
            print(f"Primary Indicators:")
            for indicator in result['explanation']['primary_indicators']:
                print(f"  • {indicator}")
            print(f"\nConfidence Factors:")
            for factor, score in result['explanation']['confidence_factors'].items():
                print(f"  • {factor}: {score:.2%}")
        else:
            print(f"\n❌ Error: {response.status_code}")
            print(response.json())
    
    except FileNotFoundError:
        print(f"❌ Error: Audio file not found at {audio_path}")
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to API. Make sure the server is running!")
        print("   Run: python main.py")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def create_sample_audio():
    """
    Create a minimal valid MP3 file for testing
    This creates a very short silent MP3 for demonstration
    """
    # Minimal valid MP3 header (silent frame)
    mp3_header = bytes([
        0xFF, 0xFB, 0x90, 0x64, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
    ])
    
    # Create sample file
    with open('sample_audio.mp3', 'wb') as f:
        # Write header multiple times to create a longer file
        for _ in range(100):
            f.write(mp3_header)
    
    print("✅ Created sample_audio.mp3 for testing")



if __name__ == "__main__":
    print("🎙️  AI Voice Detection API - Test Client")
    print("="*60)
    
    # Check if sample audio exists, if not create one
    if not Path("sample_audio.mp3").exists():
        print("\n📝 No sample audio found. Creating test file...")
        create_sample_audio()
    
    # Test with sample audio
    print("\n🧪 Running test with sample audio...")
    test_detection("sample_audio.mp3", language="english")
    
    # Test with your own human voice
    print("\n🧪 Running test with your own human voice...")
    test_detection("human_english.mp3", language="english")
    
    print("\n" + "="*60)
    print("\n💡 To test with your own audio:")
    print("   test_detection('path/to/your/audio.mp3', language='tamil')")
    print("\n🔄 Supported languages: tamil, english, hindi, malayalam, telugu")





# if __name__ == "__main__":
#     print("🎙️  AI Voice Detection API - Test Client")
#     print("="*60)
    
#     # Check if sample audio exists, if not create one
#     if not Path("sample_audio.mp3").exists():
#         print("\n📝 No sample audio found. Creating test file...")
#         create_sample_audio()
    
#     # Test with sample audio
#     print("\n🧪 Running test...")
#     test_detection("sample_audio.mp3", language="english")
    
#     print("\n" + "="*60)
#     print("\n💡 To test with your own audio:")
#     print("   test_detection('path/to/your/audio.mp3', language='tamil')")
#     print("\n🔄 Supported languages: tamil, english, hindi, malayalam, telugu")
