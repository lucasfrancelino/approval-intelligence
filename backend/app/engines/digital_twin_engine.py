from dataclasses import dataclass


@dataclass
class DigitalTwinState:
    candidate_exam_id: int

    performance_current: float
    performance_previous: float
    performance_variation: float

    performance_direction: str
    performance_status: str

    performance_level: str
    performance_consistency: str

    evidence_count: int

    overall_status: str
    summary: str


class DigitalTwinEngine:

    def build(
        self,
        candidate_exam_id: int,
        performance,
    ) -> DigitalTwinState:

        overall_status = self._classify_overall_status(
            performance=performance,
        )

        summary = self._build_summary(
            performance=performance,
            overall_status=overall_status,
        )

        return DigitalTwinState(
            candidate_exam_id=candidate_exam_id,

            performance_current=performance.current_value,
            performance_previous=performance.previous_value,
            performance_variation=performance.variation,

            performance_direction=performance.direction,
            performance_status=performance.status,

            performance_level=performance.level,
            performance_consistency=performance.consistency,

            evidence_count=performance.evidence_count,

            overall_status=overall_status,
            summary=summary,
        )

    @staticmethod
    def _classify_overall_status(
        performance,
    ) -> str:

        if performance.evidence_count < 2:
            return "dados_insuficientes"

        if performance.status == "positivo":
            return "evolucao"

        if performance.status == "negativo":
            return "atencao"

        return "estavel"

    @staticmethod
    def _build_summary(
        performance,
        overall_status: str,
    ) -> str:

        if overall_status == "dados_insuficientes":
            return (
                "Ainda existem poucas evidências para construir "
                "um estado confiável do candidato."
            )

        if overall_status == "evolucao":
            return (
                "O candidato apresenta evolução de desempenho. "
                f"O percentual atual é de "
                f"{performance.current_value:.1f}%, "
                f"com variação de "
                f"{performance.variation:.1f} pontos percentuais "
                "nas evidências mais recentes."
            )

        if overall_status == "atencao":
            return (
                "O candidato apresenta queda de desempenho. "
                f"O percentual atual é de "
                f"{performance.current_value:.1f}%, "
                f"com variação de "
                f"{performance.variation:.1f} pontos percentuais "
                "nas evidências mais recentes."
            )

        return (
            "O desempenho do candidato permanece estável em "
            f"{performance.current_value:.1f}%, "
            f"com base em {performance.evidence_count} evidências."
        )