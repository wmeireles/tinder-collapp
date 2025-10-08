from pydantic import BaseModel
from typing import List, Optional

class CreatorProfile(BaseModel):
    nome: str
    nicho: str
    plataformas: List[str]
    publico: str
    objetivo: str
    localizacao: Optional[str] = None
    engajamento: Optional[str] = None
    estilo: Optional[str] = None

class MatchRequest(BaseModel):
    creator_a: CreatorProfile
    creator_b: CreatorProfile

class MatchResponse(BaseModel):
    match_percent: int
    motivo: str

class CollabSuggestion(BaseModel):
    titulo: str
    descricao: str
    plataforma: str
    frase_inicial_chat: str

class MediaKitRequest(BaseModel):
    nome: str
    nicho: str
    publico: str
    plataformas: List[str]
    metricas: dict
    tipos_parceria: List[str]
    contato: str
    bio: Optional[str] = None