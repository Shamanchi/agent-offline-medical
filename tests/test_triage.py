"""Unit-тесты триажа: без сети, детерминированы."""

import pytest

from app.services.symptoms import DISCLAIMER, known_symptoms, triage


def test_routine_case() -> None:
    result = triage("fever and dry cough for two days")
    assert result.urgency == "routine"
    assert result.matched == ["cough", "dry cough", "fever"]
    assert result.see_doctor is True
    assert result.disclaimer == DISCLAIMER


def test_emergency_wins() -> None:
    result = triage("chest pain and headache")
    assert result.urgency == "emergency"
    assert "chest pain" in result.matched
    assert any("emergency" in tip.lower() for tip in result.advice)


def test_self_care() -> None:
    result = triage("runny nose since morning")
    assert result.urgency == "self-care"
    assert result.see_doctor is False


def test_unknown_symptoms() -> None:
    result = triage("my left elbow squeaks")
    assert result.urgency == "routine"
    assert result.matched == []
    assert result.see_doctor is True


def test_empty_rejected() -> None:
    with pytest.raises(ValueError):
        triage("   ")


def test_catalog() -> None:
    assert "fever" in known_symptoms()
    assert "chest pain" in known_symptoms()
