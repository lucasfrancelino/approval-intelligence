from dataclasses import dataclass


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
        if evidence_type == "simulado":
            return self._interpret_simulado(value)

        raise ValueError(
            f"Tipo de evidência não suportado: {evidence_type}"
        )

    def _interpret_simulado(self, value: str) -> EvidenceInterpretation:
        percentage = self._extract_percentage(value)

        status = self._classify_percentage(percentage)

        interpretation = self._build_interpretation(
            percentage,
            status,
        )

        return EvidenceInterpretation(
            dimension="desempenho",
            metric="percentual_acerto",
            value=percentage,
            unit="percent",
            status=status,
            interpretation=interpretation,
        )

    @staticmethod
    def _extract_percentage(value: str) -> float:
        import re

        match = re.search(r"(\d+(?:[.,]\d+)?)\s*%", value)

        if not match:
            raise ValueError(
                "Não foi possível identificar um percentual na evidência."
            )

        return float(match.group(1).replace(",", "."))

    @staticmethod
    def _classify_percentage(percentage: float) -> str:
        if percentage < 50:
            return "critico"

        if percentage < 70:
            return "atencao"

        if percentage < 85:
            return "bom"

        return "excelente"

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