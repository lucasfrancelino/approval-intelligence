from dataclasses import dataclass

from app.engines.decision_engine import Decision


@dataclass
class RecommendedAction:
    operational_action: str
    instructions: str
    status: str = "recommended"


class ActionEngine:

    def translate(
        self,
        decision: Decision,
    ) -> RecommendedAction:
        translator = self._translators.get(decision.action)

        if translator is None:
            raise ValueError(
                f"Ação não suportada pelo Action Engine: {decision.action}"
            )

        return translator(decision)

    def _translate_investigar_queda_em_disciplina(
        self,
        decision: Decision,
    ) -> RecommendedAction:
        return RecommendedAction(
            operational_action="revisar_conteudos_da_dimensao",
            instructions=(
                f"Revisar os conteúdos relacionados a "
                f"{decision.target_discipline} antes de realizar "
                "um novo bloco de questões sobre o tema."
            ),
        )

    def _translate_reforcar_base(
        self,
        decision: Decision,
    ) -> RecommendedAction:
        return RecommendedAction(
            operational_action="revisar_conteudo_fundamental",
            instructions=(
                "Revisar o conteúdo fundamental das disciplinas "
                "com pior desempenho antes de avançar para "
                "questões de maior complexidade."
            ),
        )

    def _translate_revisar_pontos_fracos(
        self,
        decision: Decision,
    ) -> RecommendedAction:
        return RecommendedAction(
            operational_action="refazer_questoes_dos_pontos_fracos",
            instructions=(
                "Refazer questões dos temas com maior incidência "
                "de erro nas evidências mais recentes."
            ),
        )

    def _translate_consolidar_aprendizado(
        self,
        decision: Decision,
    ) -> RecommendedAction:
        return RecommendedAction(
            operational_action="praticar_questoes_de_fixacao",
            instructions=(
                "Praticar questões de fixação no nível atual "
                "para consolidar o aprendizado antes de avançar."
            ),
        )

    def _translate_investigar_queda(
        self,
        decision: Decision,
    ) -> RecommendedAction:
        return RecommendedAction(
            operational_action="realizar_novo_simulado",
            instructions=(
                "Realizar um novo simulado para confirmar se a "
                "queda de desempenho é uma tendência real antes "
                "de ajustar o plano de estudos."
            ),
        )

    def _translate_aumentar_desafio(
        self,
        decision: Decision,
    ) -> RecommendedAction:
        return RecommendedAction(
            operational_action="avancar_nivel_de_dificuldade",
            instructions=(
                "Avançar para questões de nível de dificuldade "
                "mais alto, mantendo o ritmo de evolução atual."
            ),
        )

    def _translate_manter_e_observar(
        self,
        decision: Decision,
    ) -> RecommendedAction:
        return RecommendedAction(
            operational_action="manter_rotina_atual",
            instructions=(
                "Manter a rotina de estudos atual e aguardar "
                "novas evidências antes de qualquer ajuste."
            ),
        )

    @property
    def _translators(self):
        return {
            "investigar_queda_em_disciplina": (
                self._translate_investigar_queda_em_disciplina
            ),
            "reforcar_base": self._translate_reforcar_base,
            "revisar_pontos_fracos": self._translate_revisar_pontos_fracos,
            "consolidar_aprendizado": self._translate_consolidar_aprendizado,
            "investigar_queda": self._translate_investigar_queda,
            "aumentar_desafio": self._translate_aumentar_desafio,
            "manter_e_observar": self._translate_manter_e_observar,
        }