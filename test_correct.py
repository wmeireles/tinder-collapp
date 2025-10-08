import requests

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZW1vQGNvbGxhcHAuY29tIiwiZXhwIjoxNzU5Nzk4MTg2fQ.7wGLrCUzHlX_EcNHqYK1Pmpz5JM2RVCCeC9pkmdEIxQ"

headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# Teste endpoint correto
wanted_data = {
    "title": "Test Post",
    "description": "Test Description", 
    "collaboration_type": "content_swap"
}

print("Testando endpoint correto /wanted/posts...")
response = requests.post("http://127.0.0.1:8000/wanted/posts", json=wanted_data, headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")

if response.status_code in [200, 201]:
    print("SUCCESS: Wanted post criado!")
else:
    print("ERROR: Falha ao criar wanted post")