from fastapi import APIRouter, Depends
from app.services.groq_service import GroqService
from app.schemas.claim import ClaimExtraction, EmailProcessRequest
from app.api import deps
from app.models.user import User

router = APIRouter()

def get_groq_service() -> GroqService:
    return GroqService()

@router.post("/process", response_model=ClaimExtraction)
def process_email(
    request: EmailProcessRequest,
    current_user: User = Depends(deps.get_current_user), 
    groq_service: GroqService = Depends(get_groq_service)
):
    return groq_service.process_claim_email(request.subject, request.body)