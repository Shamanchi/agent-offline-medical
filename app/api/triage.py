"""Эндпоинты доврачебной информации."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.symptoms import TriageResult, known_symptoms, triage

router = APIRouter()


class TriageRequest(BaseModel):
    symptoms: str = Field(min_length=1, max_length=2000)
    age: int | None = Field(default=None, ge=0, le=130)


@router.get("/symptoms")
async def symptoms() -> dict:
    return {"symptoms": known_symptoms()}


@router.post("/triage", response_model=TriageResult)
async def triage_endpoint(request: TriageRequest) -> TriageResult:
    try:
        return triage(request.symptoms)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
