import re
from dataclasses import dataclass

from app.core.classification import classify_level
from app.core.constants import (
    EVIDENCE_TYPE_SIMULADO,
    SUPPORTED_METRIC,
)


@dataclass
class EvidenceInterpretation:
    dimension: str
    metric: str
    value: float
    unit: str
    status: str
    interpretation: str


class EvidenceEngine:

    def interpret(self, evidence_type: str, value: str) -> EvidenceInterpretation:
        if evidence_type == EVIDENCE_TYPE_SIMULADO:
            return self._interpret_simulado(value)

        raise ValueError(
            f"Tipo de evidência não suportado: {evidence_type}"
        )

    def _interpret_simulado(self, value: str) -> EvidenceInterpretation:
        percentage = self._extract_percentage(value)

        status = classify_level(percentage)

        interpretation = self._build_interpretation(
            percentage,
            status,
        )

        return EvidenceInterpretation(
            dimension="desempenho",
            metric=SUPPORTED_METRIC,
            value=percentage,
            unit="percent",
            status=status,
            interpretation=interpretation,
        )

    @staticmethod
    def _extract_percentage(value: str) -> float:
        match = re.search(r"(\d+(?:[.,]\d+)?)\s*%", value)

        if not match:
            raise ValueError(
                "Não foi possível identificar um percentual na evidência."
            )

        return float(match.group(1).replace(",", "."))

    @staticmethod
    def _build_interpretation(
        percentage: float,
        status: str,
    ) -> str:
        interpretations = {
            "critico": (
                f"Desempenho de {percentage:.1f}% de acerto. "
                "O resultado indica necessidade de intervenção prioritária."
            ),
            "atencao": (
                f"Desempenho de {percentage:.1f}% de acerto. "
                "O resultado indica necessidade de reforço."
            ),
            "bom": (
                f"Desempenho de {percentage:.1f}% de acerto. "
                "O resultado indica desempenho satisfatório."
            ),
            "excelente": (
                f"Desempenho de {percentage:.1f}% de acerto. "
                "O resultado indica desempenho elevado."
            ),
        }

        return interpretations[status]