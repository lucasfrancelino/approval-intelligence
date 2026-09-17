import pytest

from app.engines.evidence_engine import (
    EvidenceEngine,
    EvidenceInterpretation,
)


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


def test_tipo_de_evidencia_e_normalizado():
    engine = EvidenceEngine()

    result = engine.interpret(
        evidence_type=" SIMULADO ",
        value="Acertou 72% das questões",
    )

    assert result.value == 72.0
    assert result.status == "bom"


def test_interpretador_customizado_pode_ser_registrado():
    engine = EvidenceEngine()

    def interpret_declarado(
        value: str,
    ) -> EvidenceInterpretation:
        return EvidenceInterpretation(
            dimension="rotina_estudo",
            metric="horas_estudo",
            value=float(value),
            unit="horas",
            status="observado",
            interpretation=(
                f"O candidato declarou {value} horas de estudo."
            ),
        )

    engine.register_interpreter(
        evidence_type="declarado",
        interpreter=interpret_declarado,
    )

    result = engine.interpret(
        evidence_type="declarado",
        value="4",
    )

    assert result.dimension == "rotina_estudo"
    assert result.metric == "horas_estudo"
    assert result.value == 4.0
    assert result.unit == "horas"
    assert result.status == "observado"


def test_tipo_de_evidencia_customizado_e_normalizado():
    engine = EvidenceEngine()

    def interpret_inferido(
        value: str,
    ) -> EvidenceInterpretation:
        return EvidenceInterpretation(
            dimension="risco",
            metric="nivel_risco",
            value=float(value),
            unit="nivel",
            status="inferido",
            interpretation="Risco inferido a partir das evidências.",
        )

    engine.register_interpreter(
        evidence_type=" INFERIDO ",
        interpreter=interpret_inferido,
    )

    result = engine.interpret(
        evidence_type="inferido",
        value="2",
    )

    assert result.metric == "nivel_risco"
    assert result.value == 2.0
    assert result.status == "inferido"


def test_percentual_com_espaco_antes_do_simbolo():
    engine = EvidenceEngine()

    result = engine.interpret(
        evidence_type="simulado",
        value="Acertou 72 % das questões",
    )

    assert result.value == 72.0
    assert result.status == "bom"


def test_percentual_por_extenso():
    engine = EvidenceEngine()

    result = engine.interpret(
        evidence_type="simulado",
        value="Acertou 72 por cento das questões",
    )

    assert result.value == 72.0
    assert result.status == "bom"


def test_percentual_por_extenso_com_decimal_e_maiuscula():
    engine = EvidenceEngine()

    result = engine.interpret(
        evidence_type="simulado",
        value="O candidato obteve 78,5 POR CENTO de aproveitamento",
    )

    assert result.value == 78.5
    assert result.status == "bom"


def test_percentual_com_simbolo_tem_prioridade_sobre_extenso():
    engine = EvidenceEngine()

    result = engine.interpret(
        evidence_type="simulado",
        value="Resultado: 65% (aproximadamente 60 por cento na prova anterior)",
    )

    assert result.value == 65.0