import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.ai.schemas import MatchRequest, CreatorProfile, MediaKitRequest
from app.ai.service import AIService

def test_match_calculation_endpoint(client: TestClient):
    # Register and login first
    client.post("/auth/register", json={"email": "test@example.com", "password": "testpass123"})
    login_response = client.post("/auth/login", json={"email": "test@example.com", "password": "testpass123"})
    token = login_response.json()["access_token"]
    
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
    
    with patch.object(AIService, 'calculate_match') as mock_match:
        mock_match.return_value = MagicMock(match_percent=87, motivo="Nichos complementares")
        
        response = client.post(
            "/ai/match",
            json=match_data,
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "match_percent" in data
        assert "motivo" in data

def test_collab_suggestion_endpoint(client: TestClient):
    # Register and login first
    client.post("/auth/register", json={"email": "test2@example.com", "password": "testpass123"})
    login_response = client.post("/auth/login", json={"email": "test2@example.com", "password": "testpass123"})
    token = login_response.json()["access_token"]
    
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
    
    with patch.object(AIService, 'suggest_collab') as mock_collab:
        mock_collab.return_value = MagicMock(
            titulo="Desafio das 24h",
            descricao="Ideia criativa",
            plataforma="Instagram Reels",
            frase_inicial_chat="Vamos colaborar?"
        )
        
        response = client.post(
            "/ai/collab-suggestion",
            json=match_data,
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "titulo" in data
        assert "descricao" in data

def test_media_kit_generation_endpoint(client: TestClient):
    # Register and login first
    client.post("/auth/register", json={"email": "test3@example.com", "password": "testpass123"})
    login_response = client.post("/auth/login", json={"email": "test3@example.com", "password": "testpass123"})
    token = login_response.json()["access_token"]
    
    media_kit_data = {
        "nome": "Ana Souza",
        "nicho": "viagem e lifestyle",
        "publico": "mulheres 20-35",
        "plataformas": ["Instagram", "TikTok"],
        "metricas": {"instagram": "85k", "tiktok": "40k"},
        "tipos_parceria": ["publiposts", "press trips"],
        "contato": "ana@exemplo.com"
    }
    
    with patch.object(AIService, 'generate_media_kit') as mock_media_kit:
        mock_media_kit.return_value = "Media Kit gerado com sucesso"
        
        response = client.post(
            "/ai/media-kit",
            json=media_kit_data,
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "media_kit" in data

def test_ai_endpoints_require_authentication(client: TestClient):
    match_data = {
        "creator_a": {"nome": "Test", "nicho": "test", "plataformas": ["Instagram"], "publico": "test", "objetivo": "test"},
        "creator_b": {"nome": "Test", "nicho": "test", "plataformas": ["Instagram"], "publico": "test", "objetivo": "test"}
    }
    
    # Test without token
    response = client.post("/ai/match", json=match_data)
    assert response.status_code == 403
    
    response = client.post("/ai/collab-suggestion", json=match_data)
    assert response.status_code == 403
    
    media_kit_data = {
        "nome": "Test", "nicho": "test", "publico": "test",
        "plataformas": ["Instagram"], "metricas": {}, "tipos_parceria": [], "contato": "test@test.com"
    }
    response = client.post("/ai/media-kit", json=media_kit_data)
    assert response.status_code == 403

@patch('openai.chat.completions.create')
def test_ai_service_match_calculation(mock_openai):
    mock_openai.return_value = MagicMock()
    mock_openai.return_value.choices = [MagicMock()]
    mock_openai.return_value.choices[0].message.content = '{"match_percent": 85, "motivo": "Nichos complementares"}'
    
    request = MatchRequest(
        creator_a=CreatorProfile(nome="Ana", nicho="viagem", plataformas=["Instagram"], publico="mulheres", objetivo="parcerias"),
        creator_b=CreatorProfile(nome="Lucas", nicho="vlogs", plataformas=["YouTube"], publico="jovens", objetivo="conteúdo")
    )
    
    with patch.object(AIService, '_load_template', return_value="Template {creator_a_nome}"):
        result = AIService.calculate_match(request)
        assert result.match_percent == 85
        assert "complementares" in result.motivo