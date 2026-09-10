import pytest

from app.engines.trend_engine import TrendEngine


def test_tendencia_de_evolucao():

    engine = TrendEngine()

    result = engine.analyze(
        values=[58.0, 64.0, 69.0, 72.0]
    )

    assert result.metric == "percentual_acerto"
    assert result.current_value == 72.0
    assert result.previous_value == 69.0
    assert result.variation == 3.0
    assert result.direction == "evolucao"
    assert result.status == "positivo"


def test_tendencia_de_queda():

    engine = TrendEngine()

    result = engine.analyze(
        values=[78.0, 74.0, 68.0]
    )

    assert result.current_value == 68.0
    assert result.previous_value == 74.0
    assert result.variation == -6.0
    assert result.direction == "queda"
    assert result.status == "negativo"


def test_tendencia_estavel():

    engine = TrendEngine()

    result = engine.analyze(
        values=[72.0, 72.0]
    )

    assert result.current_value == 72.0
    assert result.previous_value == 72.0
    assert result.variation == 0.0
    assert result.direction == "estavel"
    assert result.status == "neutro"


def test_tendencia_exige_duas_evidencias():

    engine = TrendEngine()

    with pytest.raises(ValueError):
        engine.analyze(
            values=[72.0]
        )

def test_tendencia_consistente_de_evolucao():

    engine = TrendEngine()

    result = engine.analyze(
        values=[58.0, 64.0, 69.0, 72.0]
    )

    assert result.direction == "evolucao"
    assert result.status == "positivo"


def test_tendencia_consistente_de_queda():

    engine = TrendEngine()

    result = engine.analyze(
        values=[82.0, 78.0, 74.0, 70.0]
    )

    assert result.direction == "queda"
    assert result.status == "negativo"