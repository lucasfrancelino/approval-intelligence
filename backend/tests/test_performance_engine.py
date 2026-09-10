from app.engines.performance_engine import PerformanceEngine


def test_performanceo_em_evolucao():

    engine = PerformanceEngine()

    result = engine.analyze(
        values=[58, 64, 69, 72],
    )

    assert result.current_value == 72
    assert result.previous_value == 69
    assert result.variation == 3
    assert result.direction == "evolucao"
    assert result.status == "positivo"


def test_performanceo_em_queda():

    engine = PerformanceEngine()

    result = engine.analyze(
        values=[82, 78, 74, 68],
    )

    assert result.current_value == 68
    assert result.previous_value == 74
    assert result.variation == -6
    assert result.direction == "queda"
    assert result.status == "negativo"


def test_performanceo_estavel():

    engine = PerformanceEngine()

    result = engine.analyze(
        values=[72, 72, 72],
    )

    assert result.current_value == 72
    assert result.direction == "estavel"
    assert result.status == "neutro"


def test_performanceo_exige_dois_resultados():

    engine = PerformanceEngine()

    try:
        engine.analyze(
            values=[72],
        )

        assert False, "Era esperado ValueError"

    except ValueError as error:
        assert "duas" in str(error)