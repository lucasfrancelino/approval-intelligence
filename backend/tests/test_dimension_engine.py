import pytest

from app.engines.dimension_engine import DimensionEngine


def test_dimension_evolution():
    engine = DimensionEngine()

    result = engine.analyze(
        discipline="Português",
        values=[72, 78],
    )

    assert result.discipline == "Português"
    assert result.current_value == 78
    assert result.previous_value == 72
    assert result.variation == 6
    assert result.direction == "evolucao"
    assert result.status == "positivo"
    assert result.level == "bom"
    assert result.classification == "forca"
    assert result.gap_type == "nenhum"


def test_dimension_drop():
    engine = DimensionEngine()

    result = engine.analyze(
        discipline="Matemática",
        values=[61, 55],
    )

    assert result.discipline == "Matemática"
    assert result.current_value == 55
    assert result.previous_value == 61
    assert result.variation == -6
    assert result.direction == "queda"
    assert result.status == "negativo"
    assert result.level == "atencao"
    assert result.classification == "gap"
    assert result.gap_type == "nivel_e_tendencia"


def test_dimension_stable():
    engine = DimensionEngine()

    result = engine.analyze(
        discipline="Direito",
        values=[80, 80],
    )

    assert result.discipline == "Direito"
    assert result.variation == 0
    assert result.direction == "estavel"
    assert result.status == "neutro"
    assert result.level == "bom"
    assert result.classification == "forca"
    assert result.gap_type == "nenhum"


def test_dimension_critical_level():
    engine = DimensionEngine()

    result = engine.analyze(
        discipline="Física",
        values=[45, 42],
    )

    assert result.level == "critico"
    assert result.direction == "queda"
    assert result.classification == "gap"
    assert result.gap_type == "nivel_e_tendencia"


def test_dimension_excellent_level():
    engine = DimensionEngine()

    result = engine.analyze(
        discipline="Direito",
        values=[88, 92],
    )

    assert result.level == "excelente"
    assert result.direction == "evolucao"
    assert result.classification == "forca"
    assert result.gap_type == "nenhum"


def test_dimension_excelente_em_queda_e_gap_de_tendencia():
    engine = DimensionEngine()

    result = engine.analyze(
        discipline="Português",
        values=[93, 88],
    )

    assert result.level == "excelente"
    assert result.direction == "queda"
    assert result.classification == "gap"
    assert result.gap_type == "tendencia"


def test_dimension_atencao_sem_queda_e_gap_de_nivel():
    engine = DimensionEngine()

    result = engine.analyze(
        discipline="Raciocínio Lógico",
        values=[55, 60],
    )

    assert result.level == "atencao"
    assert result.direction == "evolucao"
    assert result.classification == "gap"
    assert result.gap_type == "nivel"


def test_dimension_requires_two_evidences():
    engine = DimensionEngine()

    with pytest.raises(ValueError):
        engine.analyze(
            discipline="Português",
            values=[80],
        )