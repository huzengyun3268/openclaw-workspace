import os
import base64
import requests
import json

api_key = os.environ.get("MINIMAX_API_KEY", "")
if not api_key:
    print("No MINIMAX_API_KEY found")
    exit(1)

print(f"Key prefix: {api_key[:12]}...")

# Test with a simple text-to-image first
url = "https://api.minimax.chat/v1/image_generations"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}
payload = {
    "model": "image-01",
    "prompt": "A beautiful mountain landscape at sunset",
    "image_size": "1024x1024",
    "numbers": 1
}

try:
    r = requests.post(url, headers=headers, json=payload, timeout=30)
    print(f"Status: {r.status_code}")
    print(f"Response: {r.text[:500]}")
except Exception as e:
    print(f"Error: {e}")
