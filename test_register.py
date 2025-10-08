import requests

# Teste registro com dados válidos
user_data = {
    "email": "teste@exemplo.com",
    "password": "123456"
}

response = requests.post("http://127.0.0.1:8000/auth/register", json=user_data)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")

# Teste com email inválido
invalid_data = {
    "email": "email-invalido",
    "password": "123456"
}

response2 = requests.post("http://127.0.0.1:8000/auth/register", json=invalid_data)
print(f"\nTeste email inválido:")
print(f"Status: {response2.status_code}")
print(f"Response: {response2.text}")