from types import SimpleNamespace

from app.engines.digital_twin_engine import DigitalTwinEngine


def build_performance(
    current_value=72.0,
    previous_value=69.0,
    variation=3.0,
    direction="evolucao",
    status="positivo",
    evidence_count=4,
    consistency="consistente_evolucao",
    level="bom",
):
    return SimpleNamespace(
        current_value=current_value,
        previous_value=previous_value,
        variation=variation,
        direction=direction,
        status=status,
        evidence_count=evidence_count,
        consistency=consistency,
        level=level,
    )


def test_digital_twin_com_evolucao():

    engine = DigitalTwinEngine()

    performance = build_performance()

    disciplines = [
        SimpleNamespace(
            discipline="Português",
            current_value=88.0,
            previous_value=93.0,
            variation=-5.0,
            direction="queda",
            status="negativo",
            level="excelente",
        )
    ]

    result = engine.build(
        candidate_exam_id=1,
        performance=performance,
        disciplines=disciplines,
    )

    assert result.candidate_exam_id == 1

    assert result.performance_current == 72.0
    assert result.performance_previous == 69.0
    assert result.performance_variation == 3.0

    assert result.performance_direction == "evolucao"
    assert result.performance_status == "positivo"

    assert result.performance_level == "bom"
    assert result.performance_consistency == "consistente_evolucao"

    assert result.evidence_count == 4
    assert result.overall_status == "evolucao"

    assert result.disciplines == disciplines


def test_digital_twin_com_disciplinas_vazias_por_padrao():

    engine = DigitalTwinEngine()

    performance = build_performance()

    result = engine.build(
        candidate_exam_id=1,
        performance=performance,
    )

    assert result.disciplines == []


def test_digital_twin_com_queda():

    engine = DigitalTwinEngine()

    performance = build_performance(
        current_value=68.0,
        previous_value=74.0,
        variation=-6.0,
        direction="queda",
        status="negativo",
        evidence_count=3,
        consistency="consistente_queda",
        level="atencao",
    )

    result = engine.build(
        candidate_exam_id=1,
        performance=performance,
    )

    assert result.performance_level == "atencao"
    assert result.performance_consistency == "consistente_queda"
    assert result.overall_status == "atencao"


def test_digital_twin_com_poucas_evidencias():

    engine = DigitalTwinEngine()

    performance = build_performance(
        current_value=72.0,
        previous_value=72.0,
        variation=0.0,
        direction="estavel",
        status="neutro",
        evidence_count=1,
        consistency="insuficiente",
        level="bom",
    )

    result = engine.build(
        candidate_exam_id=1,
        performance=performance,
    )

    assert result.overall_status == "dados_insuficientes"