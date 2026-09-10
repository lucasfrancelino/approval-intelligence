from dataclasses import dataclass


@dataclass
class PerformanceAnalysis:
    current_value: float
    previous_value: float
    variation: float

    direction: str
    status: str

    evidence_count: int

    consistency: str
    level: str


class PerformanceEngine:

    def analyze(
        self,
        values: list[float],
    ) -> PerformanceAnalysis:

        if len(values) < 2:
            raise ValueError(
                "São necessárias pelo menos duas evidências "
                "para analisar o desempenho."
            )

        current_value = values[-1]
        previous_value = values[-2]

        variation = current_value - previous_value

        direction = self._classify_direction(
            variation
        )

        status = self._classify_status(
            direction
        )

        consistency = self._classify_consistency(
            values
        )

        level = self._classify_level(
            current_value
        )

        return PerformanceAnalysis(
            current_value=current_value,
            previous_value=previous_value,
            variation=variation,
            direction=direction,
            status=status,
            evidence_count=len(values),
            consistency=consistency,
            level=level,
        )

    @staticmethod
    def _classify_direction(
        variation: float,
    ) -> str:

        if variation > 0:
            return "evolucao"

        if variation < 0:
            return "queda"

        return "estavel"

    @staticmethod
    def _classify_status(
        direction: str,
    ) -> str:

        if direction == "evolucao":
            return "positivo"

        if direction == "queda":
            return "negativo"

        return "neutro"

    @staticmethod
    def _classify_consistency(
        values: list[float],
    ) -> str:

        if len(values) < 2:
            return "insuficiente"

        variations = [
            values[index] - values[index - 1]
            for index in range(1, len(values))
        ]

        positive = sum(
            variation > 0
            for variation in variations
        )

        negative = sum(
            variation < 0
            for variation in variations
        )

        if positive == len(variations):
            return "consistente_evolucao"

        if negative == len(variations):
            return "consistente_queda"

        if positive == 0 and negative == 0:
            return "consistente_estavel"

        return "oscilante"

    @staticmethod
    def _classify_level(
        value: float,
    ) -> str:

        if value < 50:
            return "critico"

        if value < 70:
            return "atencao"

        if value < 85:
            return "bom"

        return "excelente"