"""
Exemplos de uso da API de IA do Collapp
Execute este arquivo para testar os endpoints de IA
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def register_and_login():
    # Registrar usuário
    register_data = {
        "email": "creator@example.com",
        "password": "password123"
    }
    requests.post(f"{BASE_URL}/auth/register", json=register_data)
    
    # Fazer login
    login_response = requests.post(f"{BASE_URL}/auth/login", json=register_data)
    return login_response.json()["access_token"]

def test_match_calculation(token):
    headers = {"Authorization": f"Bearer {token}"}
    
    match_data = {
        "creator_a": {
            "nome": "Ana Souza",
            "nicho": "viagem e lifestyle",
            "plataformas": ["Instagram", "TikTok"],
            "publico": "mulheres 20-35",
            "objetivo": "parcerias com marcas"
        },
        "creator_b": {
            "nome": "Lucas Ferreira",
            "nicho": "viagem e vlogs",
            "plataformas": ["YouTube", "Instagram"],
            "publico": "jovens 18-30",
            "objetivo": "criar conteúdo em dupla"
        }
    }
    
    response = requests.post(f"{BASE_URL}/ai/match", json=match_data, headers=headers)
    print("🎯 Cálculo de Match:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    print()

def test_collab_suggestion(token):
    headers = {"Authorization": f"Bearer {token}"}
    
    match_data = {
        "creator_a": {
            "nome": "Ana Souza",
            "nicho": "viagem e lifestyle",
            "plataformas": ["Instagram", "TikTok"],
            "publico": "mulheres 20-35",
            "objetivo": "parcerias com marcas"
        },
        "creator_b": {
            "nome": "Lucas Ferreira",
            "nicho": "viagem e vlogs",
            "plataformas": ["YouTube", "Instagram"],
            "publico": "jovens 18-30",
            "objetivo": "criar conteúdo em dupla"
        }
    }
    
    response = requests.post(f"{BASE_URL}/ai/collab-suggestion", json=match_data, headers=headers)
    print("💡 Sugestão de Colaboração:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    print()

def test_media_kit_generation(token):
    headers = {"Authorization": f"Bearer {token}"}
    
    media_kit_data = {
        "nome": "Ana Souza",
        "nicho": "viagem e lifestyle",
        "publico": "mulheres de 20 a 35 anos",
        "plataformas": ["Instagram", "TikTok"],
        "metricas": {
            "instagram": "85k seguidores",
            "tiktok": "40k seguidores",
            "engajamento": "5.2%"
        },
        "tipos_parceria": ["publiposts", "experiências de marca", "press trips"],
        "contato": "ana@exemplo.com",
        "bio": "Criadora de conteúdo apaixonada por viagens e lifestyle autêntico"
    }
    
    response = requests.post(f"{BASE_URL}/ai/media-kit", json=media_kit_data, headers=headers)
    print("📄 Media Kit Gerado:")
    print(response.json()["media_kit"])
    print()

if __name__ == "__main__":
    print("🚀 Testando API de IA do Collapp\n")
    
    try:
        token = register_and_login()
        print("✅ Usuário autenticado com sucesso\n")
        
        test_match_calculation(token)
        test_collab_suggestion(token)
        test_media_kit_generation(token)
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        print("Certifique-se de que a API está rodando em http://localhost:8000")