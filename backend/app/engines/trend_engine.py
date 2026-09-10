from dataclasses import dataclass


@dataclass
class TrendAnalysis:
    metric: str
    current_value: float
    previous_value: float
    variation: float
    direction: str
    status: str
    interpretation: str


class TrendEngine:

    def analyze(
        self,
        values: list[float],
        metric: str = "percentual_acerto",
    ) -> TrendAnalysis:

        if len(values) < 2:
            raise ValueError(
                "São necessárias pelo menos duas evidências para analisar uma tendência."
            )

        previous_value = values[-2]
        current_value = values[-1]

        variation = current_value - previous_value

        direction = self._classify_direction(variation)

        status = self._classify_status(direction)

        interpretation = self._build_interpretation(
            current_value=current_value,
            variation=variation,
            direction=direction,
            status=status,
        )

        return TrendAnalysis(
            metric=metric,
            current_value=current_value,
            previous_value=previous_value,
            variation=variation,
            direction=direction,
            status=status,
            interpretation=interpretation,
        )

    @staticmethod
    def _classify_direction(variation: float) -> str:

        if variation > 0:
            return "evolucao"

        if variation < 0:
            return "queda"

        return "estavel"

    @staticmethod
    def _classify_status(direction: str) -> str:

        if direction == "evolucao":
            return "positivo"

        if direction == "queda":
            return "negativo"

        return "neutro"

    @staticmethod
    def _build_interpretation(
        current_value: float,
        variation: float,
        direction: str,
        status: str,
    ) -> str:

        if direction == "evolucao":
            return (
                f"O desempenho atual é de {current_value:.1f}%. "
                f"Houve evolução de {variation:.1f} pontos percentuais "
                "em relação à evidência anterior."
            )

        if direction == "queda":
            return (
                f"O desempenho atual é de {current_value:.1f}%. "
                f"Houve queda de {abs(variation):.1f} pontos percentuais "
                "em relação à evidência anterior."
            )

        return (
            f"O desempenho atual é de {current_value:.1f}%. "
            "O resultado permanece estável em relação à evidência anterior."
        )