import requests
import json

# Criar usuário e fazer login
user_data = {
    "email": "demo@collapp.com",
    "password": "demo123"
}

# Registrar usuário
try:
    response = requests.post("http://127.0.0.1:8000/auth/register", json=user_data)
    print(f"Registro: {response.status_code}")
except:
    print("Usuário já existe")

# Fazer login
response = requests.post("http://127.0.0.1:8000/auth/login", json=user_data)
if response.status_code == 200:
    token_data = response.json()
    print(f"Token: {token_data['access_token']}")
    print(f"Use no frontend: Bearer {token_data['access_token']}")
else:
    print(f"Erro no login: {response.text}")