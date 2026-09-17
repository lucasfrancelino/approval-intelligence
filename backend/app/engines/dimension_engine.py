from dataclasses import dataclass

from app.core.classification import (
    classify_direction,
    classify_level,
    classify_status,
)


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

        direction = classify_direction(variation)
        status = classify_status(direction)
        level = classify_level(current_value)

        return DimensionAnalysis(
            dimension=dimension,
            current_value=current_value,
            previous_value=previous_value,
            variation=variation,
            direction=direction,
            status=status,
            level=level,
        )