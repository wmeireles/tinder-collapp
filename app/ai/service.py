import json
import openai
from typing import Dict, Any
from app.core.config import settings
from app.ai.schemas import MatchRequest, MatchResponse, CollabSuggestion, MediaKitRequest

openai.api_key = settings.OPENAI_API_KEY

class AIService:
    @staticmethod
    def _load_template(template_name: str) -> str:
        with open(f"app/ai/templates/{template_name}", "r", encoding="utf-8") as f:
            return f.read()
    
    @staticmethod
    def _call_openai(prompt: str) -> str:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
    
    @classmethod
    def calculate_match(cls, request: MatchRequest) -> MatchResponse:
        template = cls._load_template("match_prompt.txt")
        
        prompt = template.format(
            creator_a_nome=request.creator_a.nome,
            creator_a_nicho=request.creator_a.nicho,
            creator_a_plataformas=", ".join(request.creator_a.plataformas),
            creator_a_publico=request.creator_a.publico,
            creator_a_objetivo=request.creator_a.objetivo,
            creator_b_nome=request.creator_b.nome,
            creator_b_nicho=request.creator_b.nicho,
            creator_b_plataformas=", ".join(request.creator_b.plataformas),
            creator_b_publico=request.creator_b.publico,
            creator_b_objetivo=request.creator_b.objetivo
        )
        
        response = cls._call_openai(prompt)
        result = json.loads(response)
        return MatchResponse(**result)
    
    @classmethod
    def suggest_collab(cls, request: MatchRequest) -> CollabSuggestion:
        template = cls._load_template("collab_prompt.txt")
        
        prompt = template.format(
            creator_a_nome=request.creator_a.nome,
            creator_a_nicho=request.creator_a.nicho,
            creator_a_plataformas=", ".join(request.creator_a.plataformas),
            creator_a_publico=request.creator_a.publico,
            creator_a_objetivo=request.creator_a.objetivo,
            creator_b_nome=request.creator_b.nome,
            creator_b_nicho=request.creator_b.nicho,
            creator_b_plataformas=", ".join(request.creator_b.plataformas),
            creator_b_publico=request.creator_b.publico,
            creator_b_objetivo=request.creator_b.objetivo
        )
        
        response = cls._call_openai(prompt)
        result = json.loads(response)
        return CollabSuggestion(**result)
    
    @classmethod
    def generate_media_kit(cls, request: MediaKitRequest) -> str:
        template = cls._load_template("mediakit_prompt.txt")
        
        prompt = template.format(
            nome=request.nome,
            nicho=request.nicho,
            publico=request.publico,
            plataformas=", ".join(request.plataformas),
            metricas=str(request.metricas),
            tipos_parceria=", ".join(request.tipos_parceria),
            contato=request.contato,
            bio=request.bio or "Não informado"
        )
        
        return cls._call_openai(prompt)