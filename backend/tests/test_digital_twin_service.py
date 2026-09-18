from datetime import datetime
from unittest.mock import Mock, patch

from app.services.digital_twin_service import (
    get_digital_twin_service,
)


def test_desempenho_geral_calculado_como_media_das_disciplinas():
    portugues = Mock(
        discipline="Português",
        current_value=80.0,
        previous_value=70.0,
        variation=10.0,
        direction="evolucao",
        status="positivo",
        level="bom",
    )
    matematica = Mock(
        discipline="Matemática",
        current_value=60.0,
        previous_value=50.0,
        variation=10.0,
        direction="evolucao",
        status="positivo",
        level="atencao",
    )

    db = Mock()

    with patch(
        "app.services.digital_twin_service.analyze_dimensions_service",
        return_value=[portugues, matematica],
    ):
        result = get_digital_twin_service(
            db=db,
            candidate_exam_id=1,
        )

    assert result is not None
    # Média atual: (80 + 60) / 2 = 70.0
    # Média anterior: (70 + 50) / 2 = 60.0
    # Variação: 70.0 - 60.0 = +10.0
    assert result.performance_current == 70.0
    assert result.performance_previous == 60.0
    assert result.performance_variation == 10.0
    assert result.performance_direction == "evolucao"
    assert result.performance_status == "positivo"
    assert result.performance_level == "bom"
    assert len(result.dimensions) == 2


def test_desempenho_geral_usa_fallback_quando_nao_ha_disciplinas():
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
    ]

    db = Mock()

    with patch(
        "app.services.digital_twin_service.get_evidences_by_candidate_exam",
        return_value=evidences,
    ), patch(
        "app.services.digital_twin_service.analyze_dimensions_service",
        return_value=[],
    ):
        result = get_digital_twin_service(
            db=db,
            candidate_exam_id=1,
        )

    assert result is not None
    assert result.performance_current == 76.0
    assert result.performance_previous == 69.0
    assert result.performance_variation == 7.0
    assert result.dimensions == []


def test_metricas_nao_suportadas_nao_entram_no_fallback():
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
        "app.services.digital_twin_service.get_evidences_by_candidate_exam",
        return_value=evidences,
    ), patch(
        "app.services.digital_twin_service.analyze_dimensions_service",
        return_value=[],
    ):
        result = get_digital_twin_service(
            db=db,
            candidate_exam_id=1,
        )

    assert result is not None
    assert result.performance_current == 75.0
    assert result.performance_previous == 70.0
    assert result.performance_variation == 5.0


def test_desempenho_geral_retorna_none_se_dados_insuficientes_no_fallback():
    evidences = [
        Mock(
            evidence_type="simulado",
            discipline="geral",
            metric="percentual_acerto",
            value="Acertou 70% das questões",
            observed_at=datetime(2026, 1, 1),
        ),
    ]

    db = Mock()

    with patch(
        "app.services.digital_twin_service.get_evidences_by_candidate_exam",
        return_value=evidences,
    ), patch(
        "app.services.digital_twin_service.analyze_dimensions_service",
        return_value=[],
    ):
        result = get_digital_twin_service(
            db=db,
            candidate_exam_id=1,
        )

    assert result is None