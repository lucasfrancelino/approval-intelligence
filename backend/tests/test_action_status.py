import pytest

from app.engines.action_status import validate_transition


def test_recommended_pode_ir_para_in_progress():
    validate_transition(
        current_status="recommended",
        new_status="in_progress",
    )


def test_recommended_pode_ser_cancelada():
    validate_transition(
        current_status="recommended",
        new_status="cancelled",
    )


def test_in_progress_pode_ser_concluida():
    validate_transition(
        current_status="in_progress",
        new_status="completed",
    )


def test_in_progress_pode_ser_cancelada():
    validate_transition(
        current_status="in_progress",
        new_status="cancelled",
    )


def test_completed_nao_pode_mudar():
    with pytest.raises(ValueError):
        validate_transition(
            current_status="completed",
            new_status="in_progress",
        )


def test_cancelled_nao_pode_mudar():
    with pytest.raises(ValueError):
        validate_transition(
            current_status="cancelled",
            new_status="in_progress",
        )


def test_status_invalido():
    with pytest.raises(ValueError):
        validate_transition(
            current_status="recommended",
            new_status="invalid_status",
        )