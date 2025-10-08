#!/usr/bin/env python3

import requests
import json

def quick_login():
    base_url = "http://127.0.0.1:8000"
    
    # Try login with existing user
    login_data = {
        "email": "demo@collapp.com",
        "password": "demo123"  # Common demo password
    }
    
    print("Testing login with demo@collapp.com...")
    response = requests.post(f"{base_url}/auth/login", json=login_data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        token = data.get("access_token")
        print(f"Success! Token: {token}")
        print(f"Copy this token to localStorage: {token}")
        
        # Test the token
        headers = {"Authorization": f"Bearer {token}"}
        test_response = requests.get(f"{base_url}/auth/me", headers=headers)
        print(f"Token test: {test_response.status_code}")
        if test_response.status_code == 200:
            user_data = test_response.json()
            print(f"User: {user_data}")
    else:
        print(f"Login failed: {response.text}")
        
        # Try with test user
        login_data["email"] = "test@example.com"
        login_data["password"] = "testpass123"
        print("\nTrying test@example.com...")
        response = requests.post(f"{base_url}/auth/login", json=login_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            print(f"Success! Token: {token}")

if __name__ == "__main__":
    quick_login()