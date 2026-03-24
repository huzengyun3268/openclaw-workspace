import os
import requests

api_key = os.environ.get("MINIMAX_API_KEY", "")
url = "https://api.minimax.chat/v1/text_to_image"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}
payload = {
    "model": "image-01",
    "prompt": "A beautiful mountain landscape",
    "num_images": 1
}

try:
    r = requests.post(url, headers=headers, json=payload, timeout=30)
    print(f"Status: {r.status_code}")
    print(f"Response: {r.text[:800]}")
except Exception as e:
    print(f"Error: {e}")
