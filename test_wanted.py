import requests
import json

# Token do usuário logado
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZW1vQGNvbGxhcHAuY29tIiwiZXhwIjoxNzU5Nzk4MTg2fQ.7wGLrCUzHlX_EcNHqYK1Pmpz5JM2RVCCeC9pkmdEIxQ"

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Teste criar wanted post
wanted_data = {
    "title": "Procuro creator de Tech para collab",
    "description": "Estou criando conteúdo sobre programação e procuro parceiros",
    "collaboration_type": "content_swap",
    "requirements": "Mínimo 10k seguidores",
    "deadline": "2024-12-31T23:59:59"
}

print("Testando criação de wanted post...")
response = requests.post("http://127.0.0.1:8000/wanted/posts", json=wanted_data, headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")

if response.status_code == 200:
    print("✅ Wanted post criado com sucesso!")
else:
    print("❌ Erro ao criar wanted post")