import requests
import json

BASE_URL = "http://127.0.0.1:8000"

# Test user credentials
test_user = {
    "email": "test@example.com",
    "password": "password123"
}

def register_user():
    """Register a new test user"""
    response = requests.post(f"{BASE_URL}/auth/register", json=test_user)
    if response.status_code == 200:
        print("✅ User registered successfully")
        return True
    elif response.status_code == 400 and "already registered" in response.text:
        print("ℹ️ User already exists")
        return True
    else:
        print(f"❌ Registration failed: {response.text}")
        return False

def login_user():
    """Login and get access token"""
    response = requests.post(f"{BASE_URL}/auth/login", json=test_user)
    if response.status_code == 200:
        token_data = response.json()
        print("✅ Login successful")
        return token_data["access_token"]
    else:
        print(f"❌ Login failed: {response.text}")
        return None

def test_protected_endpoint(token):
    """Test accessing a protected endpoint"""
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test /matching/discover
    response = requests.get(f"{BASE_URL}/matching/discover", headers=headers)
    print(f"📡 /matching/discover: {response.status_code}")
    
    # Test /matching/matches
    response = requests.get(f"{BASE_URL}/matching/matches", headers=headers)
    print(f"📡 /matching/matches: {response.status_code}")
    
    # Test /chat/chats
    response = requests.get(f"{BASE_URL}/chat/chats", headers=headers)
    print(f"📡 /chat/chats: {response.status_code}")

if __name__ == "__main__":
    print("🚀 Testing authentication flow...\n")
    
    # Step 1: Register user
    if register_user():
        # Step 2: Login
        token = login_user()
        if token:
            print(f"🔑 Access token: {token[:50]}...\n")
            # Step 3: Test protected endpoints
            test_protected_endpoint(token)
        else:
            print("❌ Cannot proceed without token")
    else:
        print("❌ Cannot proceed without registration")