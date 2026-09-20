"""Таблица симптомов: уровни срочности и советы. Без сети."""

from __future__ import annotations

from pydantic import BaseModel

DISCLAIMER = (
    "Informational only, not a diagnosis. "
    "If in doubt, contact a doctor or emergency services."
)

# Симптом -> (urgency, советы). Порядок срочности: emergency > urgent > routine > self-care.
SYMPTOMS: dict[str, tuple[str, list[str]]] = {
    "chest pain": ("emergency", ["Call emergency services now", "Do not drive yourself"]),
    "difficulty breathing": ("emergency", ["Call emergency services now", "Sit upright, stay calm"]),
    "severe bleeding": ("emergency", ["Apply pressure, call emergency services"]),
    "high fever": ("urgent", ["See a doctor today", "Drink fluids, rest"]),
    "fever": ("routine", ["Rest and fluids", "Monitor temperature"]),
    "dry cough": ("routine", ["Rest and fluids", "Humidify the air"]),
    "cough": ("routine", ["Rest and fluids", "Humidify the air"]),
    "headache": ("routine", ["Rest in a dark room", "Drink water"]),
    "sore throat": ("routine", ["Warm drinks", "Rest your voice"]),
    "runny nose": ("self-care", ["Blow gently, stay hydrated"]),
    "mild cold": ("self-care", ["Rest, fluids, vitamin C foods"]),
    "sprain": ("routine", ["Rest, ice, compression, elevation", "See a doctor if swelling grows"]),
    "rash": ("routine", ["Avoid scratching", "See a doctor if it spreads"]),
}

URGENCY_RANK = {"self-care": 0, "routine": 1, "urgent": 2, "emergency": 3}


class TriageResult(BaseModel):
    urgency: str
    matched: list[str]
    advice: list[str]
    see_doctor: bool
    disclaimer: str


def known_symptoms() -> list[str]:
    return sorted(SYMPTOMS)


def triage(text: str) -> TriageResult:
    """Оценить симптомы. Детерминировано."""
    if not text or not text.strip():
        raise ValueError("symptoms must not be empty")
    lowered = text.lower()
    matched = sorted(symptom for symptom in SYMPTOMS if symptom in lowered)
    if not matched:
        return TriageResult(
            urgency="routine",
            matched=[],
            advice=["No known symptoms matched", "See a doctor if you feel worse"],
            see_doctor=True,
            disclaimer=DISCLAIMER,
        )
    best = max(matched, key=lambda symptom: URGENCY_RANK[SYMPTOMS[symptom][0]])
    urgency = SYMPTOMS[best][0]
    tips: list[str] = []
    for symptom in matched:
        for tip in SYMPTOMS[symptom][1]:
            if tip not in tips:
                tips.append(tip)
    return TriageResult(
        urgency=urgency,
        matched=matched,
        advice=tips,
        see_doctor=urgency in ("emergency", "urgent", "routine"),
        disclaimer=DISCLAIMER,
    )
