from types import SimpleNamespace

from app.engines.decision_engine import DecisionEngine


def build_twin(level: str, direction: str):
    return SimpleNamespace(
        performance_level=level,
        performance_direction=direction,
        disciplines=[],
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


def test_decision_considera_queda_em_uma_dimensao():
    engine = DecisionEngine()

    digital_twin = SimpleNamespace(
        performance_level="excelente",
        performance_direction="evolucao",
        disciplines=[
            SimpleNamespace(
                discipline="Português",
                current_value=88.0,
                previous_value=93.0,
                variation=-5.0,
                direction="queda",
                status="negativo",
                level="excelente",
            )
        ],
    )

    result = engine.decide(
        digital_twin=digital_twin,
    )

    assert result.decision_type == "monitoramento_dimensao"
    assert result.priority == "media"
    assert result.action == "investigar_queda_em_disciplina"


def test_decision_dimensao_excelente_em_queda():
    engine = DecisionEngine()
    digital_twin = SimpleNamespace(
        performance_level="excelente",
        performance_direction="evolucao",
        disciplines=[
            SimpleNamespace(
                discipline="Português",
                current_value=88.0,
                previous_value=93.0,
                variation=-5.0,
                direction="queda",
                status="negativo",
                level="excelente",
            )
        ],
    )
    result = engine.decide(
        digital_twin=digital_twin,
    )
    assert result.priority == "media"
    assert result.action == "investigar_queda_em_disciplina"


def test_decision_dimensao_critica_em_queda():
    engine = DecisionEngine()
    digital_twin = SimpleNamespace(
        performance_level="excelente",
        performance_direction="evolucao",
        disciplines=[
            SimpleNamespace(
                discipline="Matemática",
                current_value=48.0,
                previous_value=72.0,
                variation=-24.0,
                direction="queda",
                status="negativo",
                level="critico",
            )
        ],
    )
    result = engine.decide(
        digital_twin=digital_twin,
    )
    assert result.priority == "alta"
    assert result.action == "investigar_queda_em_disciplina"


def test_decision_seleciona_dimensao_de_maior_prioridade():

    engine = DecisionEngine()

    digital_twin = SimpleNamespace(
        performance_level="excelente",
        performance_direction="evolucao",
        disciplines=[
            SimpleNamespace(
                discipline="Português",
                current_value=88.0,
                previous_value=93.0,
                variation=-5.0,
                direction="queda",
                status="negativo",
                level="excelente",
            ),
            SimpleNamespace(
                discipline="Matemática",
                current_value=48.0,
                previous_value=72.0,
                variation=-24.0,
                direction="queda",
                status="negativo",
                level="critico",
            ),
        ],
    )

    result = engine.decide(
        digital_twin=digital_twin,
    )

    assert result.priority == "alta"
    assert result.action == "investigar_queda_em_disciplina"
    assert "Matemática" in result.reason


def test_decision_em_empate_seleciona_maior_queda():

    engine = DecisionEngine()

    digital_twin = SimpleNamespace(
        performance_level="excelente",
        performance_direction="evolucao",
        disciplines=[
            SimpleNamespace(
                discipline="Português",
                current_value=88.0,
                previous_value=93.0,
                variation=-5.0,
                direction="queda",
                status="negativo",
                level="bom",
            ),
            SimpleNamespace(
                discipline="Direito",
                current_value=72.0,
                previous_value=80.0,
                variation=-8.0,
                direction="queda",
                status="negativo",
                level="bom",
            ),
        ],
    )

    result = engine.decide(
        digital_twin=digital_twin,
    )

    assert result.priority == "media"
    assert result.action == "investigar_queda_em_disciplina"
    assert "Direito" in result.reason