from datetime import datetime
from unittest.mock import Mock, patch

from app.services.digital_twin_service import (
    get_digital_twin_service,
)


def test_desempenho_geral_nao_deve_ser_contaminado_por_dimensoes():

    evidences = [
        Mock(
            evidence_type="simulado",
            discipline="geral",
            metric="percentual_acerto",
            value="Acertou 72% das questões",
            observed_at=datetime(2026, 1, 1),
        ),
        Mock(
            evidence_type="simulado",
            discipline="Português",
            metric="percentual_acerto",
            value="Acertou 93% das questões de Português",
            observed_at=datetime(2026, 1, 2),
        ),
        Mock(
            evidence_type="simulado",
            discipline="geral",
            metric="percentual_acerto",
            value="Acertou 64% das questões",
            observed_at=datetime(2026, 1, 3),
        ),
        Mock(
            evidence_type="simulado",
            discipline="geral",
            metric="percentual_acerto",
            value="Acertou 69% das questões",
            observed_at=datetime(2026, 1, 4),
        ),
        Mock(
            evidence_type="simulado",
            discipline="geral",
            metric="percentual_acerto",
            value="Acertou 76% das questões",
            observed_at=datetime(2026, 1, 5),
        ),
        Mock(
            evidence_type="simulado",
            discipline="Português",
            metric="percentual_acerto",
            value="Acertou 88% das questões de Português",
            observed_at=datetime(2026, 1, 6),
        ),
    ]

    db = Mock()

    with patch(
        "app.services.digital_twin_service."
        "get_evidences_by_candidate_exam",
        return_value=evidences,
    ), patch(
        "app.services.digital_twin_service."
        "analyze_dimensions_service",
        return_value=[
            Mock(
                discipline="Português",
                current_value=88.0,
                previous_value=93.0,
                variation=-5.0,
                direction="queda",
                status="negativo",
                level="excelente",
            )
        ],
    ):

        result = get_digital_twin_service(
            db=db,
            candidate_exam_id=1,
        )

    assert result.performance_current == 76.0
    assert result.performance_previous == 69.0
    assert result.performance_variation == 7.0

    dimensions = {
        dimension.discipline: dimension
        for dimension in result.dimensions
    }

    assert "geral" not in dimensions
    assert dimensions["Português"].current_value == 88.0


def test_metricas_nao_suportadas_nao_entram_no_desempenho_geral():

    evidences = [
        Mock(
            evidence_type="simulado",
            discipline="geral",
            metric="percentual_acerto",
            value="Acertou 70% das questões",
            observed_at=datetime(2026, 1, 1),
        ),
        Mock(
            evidence_type="simulado",
            discipline="geral",
            metric="tempo_medio",
            value="Tempo médio de 90 segundos",
            observed_at=datetime(2026, 1, 2),
        ),
        Mock(
            evidence_type="simulado",
            discipline="geral",
            metric="percentual_acerto",
            value="Acertou 75% das questões",
            observed_at=datetime(2026, 1, 3),
        ),
    ]

    db = Mock()

    with patch(
        "app.services.digital_twin_service."
        "get_evidences_by_candidate_exam",
        return_value=evidences,
    ), patch(
        "app.services.digital_twin_service."
        "analyze_dimensions_service",
        return_value=[],
    ):

        result = get_digital_twin_service(
            db=db,
            candidate_exam_id=1,
        )

    assert result.performance_current == 75.0
    assert result.performance_previous == 70.0
    assert result.performance_variation == 5.0