from types import SimpleNamespace
from unittest.mock import Mock, patch

from app.engines.decision_engine import DecisionEngine
from app.services.digital_twin_service import (
    get_digital_twin_service,
)


def test_fluxo_real_do_digital_twin_ate_a_decisao_dimensional():

    evidences = [
        Mock(
            evidence_type="simulado",
            discipline="geral",
            metric="percentual_acerto",
            value="Acertou 69% das questões",
        ),
        Mock(
            evidence_type="simulado",
            discipline="geral",
            metric="percentual_acerto",
            value="Acertou 76% das questões",
        ),
    ]

    portuguese_analysis = SimpleNamespace(
        discipline="Português",
        current_value=88.0,
        previous_value=93.0,
        variation=-5.0,
        direction="queda",
        status="negativo",
        level="excelente",
    )

    with patch(
        "app.services.digital_twin_service."
        "get_evidences_by_candidate_exam",
        return_value=evidences,
    ), patch(
        "app.services.digital_twin_service."
        "analyze_dimensions_service",
        return_value=[portuguese_analysis],
    ):

        digital_twin = get_digital_twin_service(
            db=Mock(),
            candidate_exam_id=1,
        )

    assert digital_twin.disciplines
    assert digital_twin.disciplines[0].discipline == "Português"

    decision = DecisionEngine().decide(
        digital_twin=digital_twin,
    )

    assert decision.decision_type == "monitoramento_dimensao"
    assert decision.priority == "media"
    assert decision.action == "investigar_queda_em_disciplina"
    assert decision.target_discipline == "Português"
    assert "Português" in decision.reason