from dataclasses import dataclass


@dataclass
class Decision:
    decision_type: str
    priority: str
    action: str
    reason: str


class DecisionEngine:

    def decide(self, digital_twin) -> Decision:

        if digital_twin.performance_level == "critico":
            return Decision(
                decision_type="intervencao_desempenho",
                priority="alta",
                action="reforcar_base",
                reason=(
                    "O desempenho atual está em nível crítico. "
                    "A prioridade deve ser reforçar a base de conhecimento "
                    "antes de aumentar a complexidade das atividades."
                ),
            )

        if (
            digital_twin.performance_level == "atencao"
            and digital_twin.performance_direction == "queda"
        ):
            return Decision(
                decision_type="correcao_desempenho",
                priority="alta",
                action="revisar_pontos_fracos",
                reason=(
                    "O candidato apresenta desempenho abaixo do nível desejado "
                    "e tendência de queda. A prioridade deve ser revisar "
                    "os pontos que estão contribuindo para a perda de desempenho."
                ),
            )

        if (
            digital_twin.performance_level == "atencao"
            and digital_twin.performance_direction == "evolucao"
        ):
            return Decision(
                decision_type="consolidacao",
                priority="media",
                action="consolidar_aprendizado",
                reason=(
                    "O desempenho ainda exige atenção, mas apresenta evolução. "
                    "A prioridade deve ser consolidar o aprendizado "
                    "sem interromper a trajetória de evolução."
                ),
            )

        if (
            digital_twin.performance_level in {"bom", "excelente"}
            and digital_twin.performance_direction == "queda"
        ):
            return Decision(
                decision_type="monitoramento",
                priority="media",
                action="investigar_queda",
                reason=(
                    "O nível atual de desempenho é positivo, porém existe "
                    "uma tendência recente de queda. É necessário investigar "
                    "a causa antes de aumentar a carga ou complexidade."
                ),
            )

        if (
            digital_twin.performance_level in {"bom", "excelente"}
            and digital_twin.performance_direction == "evolucao"
        ):
            return Decision(
                decision_type="progressao",
                priority="baixa",
                action="aumentar_desafio",
                reason=(
                    "O candidato apresenta bom desempenho e evolução. "
                    "A próxima ação pode aumentar gradualmente "
                    "o nível de desafio."
                ),
            )

        return Decision(
            decision_type="estabilizacao",
            priority="media",
            action="manter_e_observar",
            reason=(
                "O desempenho atual não apresenta uma condição suficiente "
                "para uma intervenção mais específica. "
                "O estado deve ser monitorado."
            ),
        )