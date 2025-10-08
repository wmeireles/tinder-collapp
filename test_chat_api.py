import requests
import json

# Test the chat API
base_url = "http://127.0.0.1:8000"

# First, let's test if the server is running
try:
    response = requests.get(f"{base_url}/health")
    print(f"Health check: {response.status_code} - {response.json()}")
except Exception as e:
    print(f"Server not running: {e}")
    exit(1)

# Test login to get token
login_data = {
    "email": "demo@collapp.com",
    "password": "demo123"
}

try:
    response = requests.post(f"{base_url}/auth/login", json=login_data)
    if response.status_code == 200:
        token = response.json()["access_token"]
        print(f"Login successful, token: {token[:20]}...")
        
        # Test chat endpoint
        headers = {"Authorization": f"Bearer {token}"}
        chat_response = requests.get(f"{base_url}/chat/chats", headers=headers)
        print(f"Chat API: {chat_response.status_code}")
        if chat_response.status_code == 200:
            chats = chat_response.json()
            print(f"Found {len(chats)} chats")
            for chat in chats:
                print(f"  Chat ID: {chat['id']}, Wanted ID: {chat.get('wanted_id', 'None')}")
        else:
            print(f"Chat API error: {chat_response.text}")
    else:
        print(f"Login failed: {response.status_code} - {response.text}")
except Exception as e:
    print(f"Error: {e}")