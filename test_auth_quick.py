#!/usr/bin/env python3

import requests
import json

# Test authentication
def test_auth():
    base_url = "http://127.0.0.1:8000"
    
    # Try to register a test user
    register_data = {
        "email": "test@example.com",
        "password": "testpass123"
    }
    
    print("1. Registering test user...")
    try:
        response = requests.post(f"{base_url}/auth/register", json=register_data)
        print(f"Register response: {response.status_code}")
        if response.status_code == 200:
            print("User registered successfully")
        else:
            print(f"Register failed: {response.text}")
    except Exception as e:
        print(f"Register error: {e}")
    
    # Try to login
    print("\n2. Logging in...")
    try:
        response = requests.post(f"{base_url}/auth/login", json=register_data)
        print(f"Login response: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            print(f"Login successful, token: {token[:20]}...")
            
            # Test authenticated endpoint
            print("\n3. Testing authenticated endpoint...")
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.post(f"{base_url}/wanted/applications", 
                                   json={"wanted_post_id": "test", "message": "test"}, 
                                   headers=headers)
            print(f"Application response: {response.status_code}")
            print(f"Response: {response.text}")
            
        else:
            print(f"Login failed: {response.text}")
    except Exception as e:
        print(f"Login error: {e}")

if __name__ == "__main__":
    test_auth()