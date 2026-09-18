from dataclasses import dataclass

from app.core.classification import (
    classify_direction,
    classify_level,
    classify_status,
)


@dataclass
class DisciplineAnalysis:
    discipline: str
    current_value: float
    previous_value: float
    variation: float
    direction: str
    status: str
    level: str
    classification: str
    gap_type: str


class DimensionEngine:
    def analyze(
        self,
        discipline: str,
        values: list[float],
    ) -> DisciplineAnalysis:
        if len(values) < 2:
            raise ValueError(
                "São necessárias pelo menos duas evidências "
                "para analisar uma disciplina."
            )

        current_value = values[-1]
        previous_value = values[-2]
        variation = current_value - previous_value

        direction = classify_direction(variation)
        status = classify_status(direction)
        level = classify_level(current_value)

        classification, gap_type = self._classify_strength_or_gap(
            level=level,
            direction=direction,
        )

        return DisciplineAnalysis(
            discipline=discipline,
            current_value=current_value,
            previous_value=previous_value,
            variation=variation,
            direction=direction,
            status=status,
            level=level,
            classification=classification,
            gap_type=gap_type,
        )

    @staticmethod
    def _classify_strength_or_gap(
        level: str,
        direction: str,
    ) -> tuple[str, str]:
        is_low_level = level in {"critico", "atencao"}
        is_dropping = direction == "queda"

        if is_low_level and is_dropping:
            return "gap", "nivel_e_tendencia"

        if is_low_level:
            return "gap", "nivel"

        if is_dropping:
            return "gap", "tendencia"

        return "forca", "nenhum"