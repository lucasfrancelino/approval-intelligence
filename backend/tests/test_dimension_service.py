from types import SimpleNamespace
from unittest.mock import patch

from app.services.dimension_service import analyze_dimensions_service


def test_analyze_dimensions_service():
    evidences = [
        SimpleNamespace(
            evidence_type="simulado",
            discipline="Matemática",
            metric="percentual_acerto",
            value="Acertou 61% das questões no último simulado",
        ),
        SimpleNamespace(
            evidence_type="simulado",
            discipline="Matemática",
            metric="percentual_acerto",
            value="Acertou 55% das questões no último simulado",
        ),
        SimpleNamespace(
            evidence_type="simulado",
            discipline="Português",
            metric="percentual_acerto",
            value="Acertou 72% das questões no último simulado",
        ),
        SimpleNamespace(
            evidence_type="simulado",
            discipline="Português",
            metric="percentual_acerto",
            value="Acertou 78% das questões no último simulado",
        ),
    ]

    with patch(
        "app.services.dimension_service."
        "get_evidences_by_candidate_exam",
        return_value=evidences,
    ):
        result = analyze_dimensions_service(
            db=None,
            candidate_exam_id=1,
        )

    assert len(result) == 2

    matematica = next(
        item
        for item in result
        if item.discipline == "Matemática"
    )

    portugues = next(
        item
        for item in result
        if item.discipline == "Português"
    )

    assert matematica.current_value == 55
    assert matematica.previous_value == 61
    assert matematica.variation == -6
    assert matematica.direction == "queda"
    assert matematica.level == "atencao"

    assert portugues.current_value == 78
    assert portugues.previous_value == 72
    assert portugues.variation == 6
    assert portugues.direction == "evolucao"
    assert portugues.level == "bom"


def test_analyze_dimensions_service_with_real_text_values():
    evidences = [
        SimpleNamespace(
            evidence_type="simulado",
            discipline="Português",
            metric="percentual_acerto",
            value="Acertou 72% das questões no último simulado",
        ),
        SimpleNamespace(
            evidence_type="simulado",
            discipline="Português",
            metric="percentual_acerto",
            value="Acertou 85% das questões no último simulado",
        ),
    ]

    with patch(
        "app.services.dimension_service."
        "get_evidences_by_candidate_exam",
        return_value=evidences,
    ):
        result = analyze_dimensions_service(
            db=None,
            candidate_exam_id=1,
        )

    assert len(result) == 1

    portugues = result[0]

    assert portugues.discipline == "Português"
    assert portugues.current_value == 85
    assert portugues.previous_value == 72
    assert portugues.variation == 13
    assert portugues.direction == "evolucao"
    assert portugues.status == "positivo"
    assert portugues.level == "excelente"


def test_desempenho_geral_nao_e_exposto_como_dimensao():

    evidences = [
        SimpleNamespace(
            evidence_type="simulado",
            discipline="geral",
            metric="percentual_acerto",
            value="Acertou 72% das questões",
        ),
        SimpleNamespace(
            evidence_type="simulado",
            discipline="geral",
            metric="percentual_acerto",
            value="Acertou 78% das questões",
        ),
        SimpleNamespace(
            evidence_type="simulado",
            discipline="Português",
            metric="percentual_acerto",
            value="Acertou 72% das questões de Português",
        ),
        SimpleNamespace(
            evidence_type="simulado",
            discipline="Português",
            metric="percentual_acerto",
            value="Acertou 78% das questões de Português",
        ),
    ]

    with patch(
        "app.services.dimension_service."
        "get_evidences_by_candidate_exam",
        return_value=evidences,
    ):
        result = analyze_dimensions_service(
            db=None,
            candidate_exam_id=1,
        )

    disciplines = {
        item.discipline
        for item in result
    }

    assert "geral" not in disciplines
    assert "Português" in disciplines