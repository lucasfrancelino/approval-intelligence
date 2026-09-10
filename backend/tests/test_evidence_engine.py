import pytest

from app.engines.evidence_engine import EvidenceEngine


def test_interpret_simulado_com_72_porcento():
    engine = EvidenceEngine()

    result = engine.interpret(
        evidence_type="simulado",
        value="Acertou 72% das questões no último simulado",
    )

    assert result.dimension == "desempenho"
    assert result.metric == "percentual_acerto"
    assert result.value == 72.0
    assert result.unit == "percent"
    assert result.status == "bom"


def test_simulado_com_desempenho_critico():
    engine = EvidenceEngine()

    result = engine.interpret(
        evidence_type="simulado",
        value="Acertou 42% das questões",
    )

    assert result.status == "critico"


def test_simulado_com_desempenho_excelente():
    engine = EvidenceEngine()

    result = engine.interpret(
        evidence_type="simulado",
        value="Acertou 91% das questões",
    )

    assert result.status == "excelente"


def test_evidencia_sem_percentual():
    engine = EvidenceEngine()

    with pytest.raises(ValueError):
        engine.interpret(
            evidence_type="simulado",
            value="Foi muito bem no simulado",
        )


def test_tipo_de_evidencia_nao_suportado():
    engine = EvidenceEngine()

    with pytest.raises(ValueError):
        engine.interpret(
            evidence_type="abc",
            value="Alguma informação",
        )