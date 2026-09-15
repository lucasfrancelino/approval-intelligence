from dataclasses import dataclass


@dataclass
class DimensionAnalysis:
    dimension: str
    current_value: float
    previous_value: float
    variation: float
    direction: str
    status: str
    level: str


class DimensionEngine:

    def analyze(
        self,
        dimension: str,
        values: list[float],
    ) -> DimensionAnalysis:

        if len(values) < 2:
            raise ValueError(
                "São necessárias pelo menos duas evidências "
                "para analisar uma dimensão."
            )

        current_value = values[-1]
        previous_value = values[-2]
        variation = current_value - previous_value

        direction = self._classify_direction(variation)
        status = self._classify_status(direction)
        level = self._classify_level(current_value)

        return DimensionAnalysis(
            dimension=dimension,
            current_value=current_value,
            previous_value=previous_value,
            variation=variation,
            direction=direction,
            status=status,
            level=level,
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
    def _classify_level(value: float) -> str:
        if value < 50:
            return "critico"

        if value < 70:
            return "atencao"

        if value < 85:
            return "bom"

        return "excelente"