from unittest.mock import Mock

from app.services.evidence_service import (
    analyze_performance_trend_service,
)


def test_analisar_tendencia_de_desempenho():

    evidences = [
        Mock(
            evidence_type="simulado",
            value="Acertou 58% das questões",
        ),
        Mock(
            evidence_type="simulado",
            value="Acertou 64% das questões",
        ),
        Mock(
            evidence_type="simulado",
            value="Acertou 72% das questões",
        ),
    ]

    db = Mock()

    db.query.return_value.filter.return_value.filter.return_value.order_by.return_value.all.return_value = evidences

    result = analyze_performance_trend_service(
        db=db,
        candidate_exam_id=1,
    )

    assert result.metric == "percentual_acerto"
    assert result.current_value == 72.0
    assert result.previous_value == 64.0
    assert result.variation == 8.0
    assert result.direction == "evolucao"
    assert result.status == "positivo"