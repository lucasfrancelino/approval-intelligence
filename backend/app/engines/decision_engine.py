from dataclasses import dataclass


@dataclass
class Decision:
    decision_type: str
    priority: str
    action: str
    target_discipline: str | None
    reason: str


class DecisionEngine:
    def decide(
        self,
        digital_twin,
    ) -> Decision:
        discipline_decision = self._analyze_disciplines(
            digital_twin=digital_twin,
        )

        if discipline_decision is not None:
            return discipline_decision

        if digital_twin.performance_level == "critico":
            return Decision(
                decision_type="intervencao_desempenho",
                priority="alta",
                action="reforcar_base",
                target_discipline=None,
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
                target_discipline=None,
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
                target_discipline=None,
                reason=(
                    "O desempenho ainda exige atenção, mas apresenta evolução. "
                    "A prioridade deve ser consolidar o aprendizado."
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
                target_discipline=None,
                reason=(
                    "O nível atual de desempenho é positivo, porém existe "
                    "uma tendência recente de queda."
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
                target_discipline=None,
                reason=(
                    "O candidato apresenta bom desempenho e evolução. "
                    "A próxima ação pode aumentar gradualmente o desafio."
                ),
            )

        return Decision(
            decision_type="estabilizacao",
            priority="media",
            action="manter_e_observar",
            target_discipline=None,
            reason=(
                "O desempenho atual não apresenta condição suficiente "
                "para uma intervenção mais específica."
            ),
        )

    def _analyze_disciplines(
        self,
        digital_twin,
    ) -> Decision | None:
        disciplines = digital_twin.dimensions
        candidates = []

        for discipline in disciplines:
            if (
                discipline.direction != "queda"
                or discipline.variation >= 0
            ):
                continue

            priority = self._classify_discipline_priority(
                discipline=discipline,
            )

            candidates.append(
                (
                    priority,
                    abs(discipline.variation),
                    discipline,
                )
            )

        if not candidates:
            return None

        priority_order = {
            "alta": 3,
            "media": 2,
            "baixa": 1,
        }

        candidates.sort(
            key=lambda item: (
                priority_order[item[0]],
                item[1],
            ),
            reverse=True,
        )

        priority, _, discipline = candidates[0]

        return Decision(
            decision_type="monitoramento_dimensao",
            priority=priority,
            action="investigar_queda_em_dimensao",
            target_discipline=discipline.discipline,
            reason=(
                f"A disciplina {discipline.discipline} apresenta queda de "
                f"{abs(discipline.variation):.1f} pontos percentuais nas "
                "evidências mais recentes."
            ),
        )

    @staticmethod
    def _classify_discipline_priority(
        discipline,
    ) -> str:
        if discipline.level == "critico":
            return "alta"

        if (
            discipline.level == "atencao"
            and discipline.direction == "queda"
        ):
            return "alta"

        if discipline.level in {"bom", "excelente"}:
            return "media"

        return "baixa"