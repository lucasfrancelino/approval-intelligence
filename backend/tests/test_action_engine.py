import pytest

from app.engines.action_engine import ActionEngine
from app.engines.decision_engine import Decision


def test_traduz_investigar_queda_em_dimensao():
    engine = ActionEngine()

    decision = Decision(
        decision_type="monitoramento_dimensao",
        priority="media",
        action="investigar_queda_em_dimensao",
        target_discipline="Português",
        reason="queda detectada",
    )

    action = engine.translate(decision=decision)

    assert action.operational_action == "revisar_conteudos_da_dimensao"
    assert "Português" in action.instructions


def test_traduz_reforcar_base():
    engine = ActionEngine()

    decision = Decision(
        decision_type="intervencao_desempenho",
        priority="alta",
        action="reforcar_base",
        target_discipline=None,
        reason="desempenho critico",
    )

    action = engine.translate(decision=decision)

    assert action.operational_action == "revisar_conteudo_fundamental"


def test_traduz_revisar_pontos_fracos():
    engine = ActionEngine()

    decision = Decision(
        decision_type="correcao_desempenho",
        priority="alta",
        action="revisar_pontos_fracos",
        target_discipline=None,
        reason="queda com atencao",
    )

    action = engine.translate(decision=decision)

    assert action.operational_action == "refazer_questoes_dos_pontos_fracos"


def test_traduz_consolidar_aprendizado():
    engine = ActionEngine()

    decision = Decision(
        decision_type="consolidacao",
        priority="media",
        action="consolidar_aprendizado",
        target_discipline=None,
        reason="atencao com evolucao",
    )

    action = engine.translate(decision=decision)

    assert action.operational_action == "praticar_questoes_de_fixacao"


def test_traduz_investigar_queda():
    engine = ActionEngine()

    decision = Decision(
        decision_type="monitoramento",
        priority="media",
        action="investigar_queda",
        target_discipline=None,
        reason="bom com queda",
    )

    action = engine.translate(decision=decision)

    assert action.operational_action == "realizar_novo_simulado"


def test_traduz_aumentar_desafio():
    engine = ActionEngine()

    decision = Decision(
        decision_type="progressao",
        priority="baixa",
        action="aumentar_desafio",
        target_discipline=None,
        reason="bom com evolucao",
    )

    action = engine.translate(decision=decision)

    assert action.operational_action == "avancar_nivel_de_dificuldade"


def test_traduz_manter_e_observar():
    engine = ActionEngine()

    decision = Decision(
        decision_type="estabilizacao",
        priority="media",
        action="manter_e_observar",
        target_discipline=None,
        reason="estavel",
    )

    action = engine.translate(decision=decision)

    assert action.operational_action == "manter_rotina_atual"


def test_acao_nao_suportada_gera_erro():
    engine = ActionEngine()

    decision = Decision(
        decision_type="tipo_invalido",
        priority="baixa",
        action="acao_inexistente",
        target_discipline=None,
        reason="teste",
    )

    with pytest.raises(ValueError):
        engine.translate(decision=decision)