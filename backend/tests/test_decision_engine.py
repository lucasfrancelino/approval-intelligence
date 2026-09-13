from types import SimpleNamespace

from app.engines.decision_engine import DecisionEngine


def build_twin(level: str, direction: str):
    return SimpleNamespace(
        performance_level=level,
        performance_direction=direction,
    )


def test_critical_performance_requires_high_priority_intervention():

    engine = DecisionEngine()

    twin = build_twin(
        level="critico",
        direction="estavel",
    )

    decision = engine.decide(twin)

    assert decision.decision_type == "intervencao_desempenho"
    assert decision.priority == "alta"
    assert decision.action == "reforcar_base"


def test_attention_with_drop_requires_correction():

    engine = DecisionEngine()

    twin = build_twin(
        level="atencao",
        direction="queda",
    )

    decision = engine.decide(twin)

    assert decision.decision_type == "correcao_desempenho"
    assert decision.priority == "alta"
    assert decision.action == "revisar_pontos_fracos"


def test_attention_with_evolution_requires_consolidation():

    engine = DecisionEngine()

    twin = build_twin(
        level="atencao",
        direction="evolucao",
    )

    decision = engine.decide(twin)

    assert decision.decision_type == "consolidacao"
    assert decision.priority == "media"
    assert decision.action == "consolidar_aprendizado"


def test_good_performance_with_drop_requires_investigation():

    engine = DecisionEngine()

    twin = build_twin(
        level="bom",
        direction="queda",
    )

    decision = engine.decide(twin)

    assert decision.decision_type == "monitoramento"
    assert decision.priority == "media"
    assert decision.action == "investigar_queda"


def test_good_performance_with_evolution_allows_progression():

    engine = DecisionEngine()

    twin = build_twin(
        level="bom",
        direction="evolucao",
    )

    decision = engine.decide(twin)

    assert decision.decision_type == "progressao"
    assert decision.priority == "baixa"
    assert decision.action == "aumentar_desafio"


def test_stable_performance_requires_monitoring():

    engine = DecisionEngine()

    twin = build_twin(
        level="bom",
        direction="estavel",
    )

    decision = engine.decide(twin)

    assert decision.decision_type == "estabilizacao"
    assert decision.priority == "media"
    assert decision.action == "manter_e_observar"