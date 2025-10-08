from fastapi import APIRouter, Depends, HTTPException
from app.ai.schemas import MatchRequest, MatchResponse, CollabSuggestion, MediaKitRequest
from app.ai.service import AIService
from app.auth.dependencies import get_current_user
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ai", tags=["ai"])

@router.post("/match", response_model=MatchResponse)
def calculate_match(
    request: MatchRequest,
    current_user = Depends(get_current_user)
):
    try:
        result = AIService.calculate_match(request)
        logger.info(f"Match calculated: {result.match_percent}% between {request.creator_a.nome} and {request.creator_b.nome}")
        return result
    except Exception as e:
        logger.error(f"Error calculating match: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao calcular compatibilidade")

@router.post("/collab-suggestion", response_model=CollabSuggestion)
def suggest_collab(
    request: MatchRequest,
    current_user = Depends(get_current_user)
):
    try:
        result = AIService.suggest_collab(request)
        logger.info(f"Collab suggestion generated for {request.creator_a.nome} and {request.creator_b.nome}")
        return result
    except Exception as e:
        logger.error(f"Error generating collab suggestion: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao gerar sugestão de colaboração")

@router.post("/media-kit")
def generate_media_kit(
    request: MediaKitRequest,
    current_user = Depends(get_current_user)
):
    try:
        result = AIService.generate_media_kit(request)
        logger.info(f"Media kit generated for {request.nome}")
        return {"media_kit": result}
    except Exception as e:
        logger.error(f"Error generating media kit: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao gerar media kit")