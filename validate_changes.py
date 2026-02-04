import requests
import time
import subprocess
import sys
import os
import signal

def cleanup_server(process):
    if process:
        print("Stopping server...")
        if sys.platform == "win32":
            subprocess.call([sys.executable, "-m", "taskkill", "/F", "/T", "/PID", str(process.pid)])
        else:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)

def wait_for_server(url, timeout=10):
    start = time.time()
    while time.time() - start < timeout:
        try:
            requests.get(url)
            print("Server is up!")
            return True
        except requests.exceptions.ConnectionError:
            time.sleep(0.5)
    print("Server failed to start in time.")
    return False

def run_test():
    # Start the server
    print("Starting server...")
    server_process = subprocess.Popen(
        [sys.executable, "main.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait for server to output the key (and thus be ready-ish)
    key = None
    try:
        # Read lines to find the key
        start = time.time()
        while time.time() - start < 10:
            line = server_process.stdout.readline()
            print(f"Server Log: {line.strip()}")
            if "API Key:" in line:
                key = line.split("API Key:")[1].strip()
                print(f"Captured API Key: {key}")
                break
            if not line and server_process.poll() is not None:
                break
        
        if not key:
            print("Failed to capture API key")
            cleanup_server(server_process)
            return

        if not wait_for_server("http://localhost:8000/"):
            cleanup_server(server_process)
            return

        # 1. Test Root Path
        print("\nTest 1: Root Path")
        resp = requests.get("http://localhost:8000/")
        print(f"Root status: {resp.status_code}")
        print(f"Root content: {resp.json()}")
        if resp.status_code == 200:
            print("✅ Root path passed")
        else:
            print("❌ Root path failed")

        # 2. Test Audio URL
        print("\nTest 2: Audio URL")
        # Use a dummy small MP3 url or one that exists. Ideally we create a local file and serve it or use a public one.
        # Since we don't have internet access guaranty or a reliable external URL, maybe we can skip actual download 
        # or mock it? But `requests.get` inside main.py will fail if no internet.
        # Wait, the prompt says "localhost server... showing nothing found". 
        # For the test, I'll pass a non-existent URL and expect a 400 with "Failed to download".
        # This proves the logic branch is taken.
        headers = {"X-API-Key": key}
        payload = {
            "audio_url": "http://google.com/fake.mp3",
            "language": "english"
        }
        resp = requests.post("http://localhost:8000/api/v1/detect", json=payload, headers=headers)
        print(f"URL Test status: {resp.status_code}")
        print(f"URL Test content: {resp.json()}")
        
        # We expect 400 because URL won't work or is invalid mp3
        if resp.status_code == 400 and "Failed to download" in str(resp.content) or "404" in str(resp.content): 
             # requests.get might return 404 for google.com/fake.mp3, raise_for_status raises HTTPError, caught as Exception.
            print("✅ Audio URL logic reachable (failed as expected with bad URL)")
        else:
            print("❌ Audio URL test unexpected result")

    except Exception as e:
        print(f"Exception during test: {e}")
    finally:
        cleanup_server(server_process)

if __name__ == "__main__":
    run_test()
