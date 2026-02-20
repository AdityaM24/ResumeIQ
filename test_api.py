import requests
import os

API_URL = "http://127.0.0.1:8000/match"

def test_health():
    response = requests.get("http://127.0.0.1:8000/health")
    print("Health Check:", response.status_code, response.json())
    assert response.status_code == 200

# We'll just test the health endpoint for now to prove FastAPI is up. 
# End-to-end testing with a real PDF requires a sample PDF in the dir.

if __name__ == "__main__":
    try:
        test_health()
        print("API Health test passed!")
    except Exception as e:
        print(f"API Health test failed: {e}")
