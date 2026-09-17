from app.core.classification import (
    classify_direction,
    classify_level,
    classify_status,
)


def test_classify_direction_evolucao():
    assert classify_direction(5.0) == "evolucao"


def test_classify_direction_queda():
    assert classify_direction(-5.0) == "queda"


def test_classify_direction_estavel():
    assert classify_direction(0.0) == "estavel"


def test_classify_status_positivo():
    assert classify_status("evolucao") == "positivo"


def test_classify_status_negativo():
    assert classify_status("queda") == "negativo"


def test_classify_status_neutro():
    assert classify_status("estavel") == "neutro"


def test_classify_level_critico():
    assert classify_level(49.9) == "critico"


def test_classify_level_atencao():
    assert classify_level(50.0) == "atencao"
    assert classify_level(69.9) == "atencao"


def test_classify_level_bom():
    assert classify_level(70.0) == "bom"
    assert classify_level(84.9) == "bom"


def test_classify_level_excelente():
    assert classify_level(85.0) == "excelente"