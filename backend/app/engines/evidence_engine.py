import re
from collections.abc import Callable
from dataclasses import dataclass

from app.core.classification import classify_level
from app.core.constants import (
    EVIDENCE_TYPE_SIMULADO,
    SUPPORTED_METRIC,
)


@dataclass
class EvidenceInterpretation:
    discipline: str
    metric: str
    value: float
    unit: str
    status: str
    interpretation: str


EvidenceInterpreter = Callable[[str], EvidenceInterpretation]


class EvidenceEngine:
    def __init__(self) -> None:
        self._interpreters: dict[str, EvidenceInterpreter] = {
            EVIDENCE_TYPE_SIMULADO: self._interpret_simulado,
        }

    def register_interpreter(
        self,
        evidence_type: str,
        interpreter: EvidenceInterpreter,
    ) -> None:
        normalized_evidence_type = evidence_type.strip().lower()

        if not normalized_evidence_type:
            raise ValueError(
                "O tipo de evidência não pode ser vazio."
            )

        self._interpreters[normalized_evidence_type] = interpreter

    def interpret(
        self,
        evidence_type: str,
        value: str,
    ) -> EvidenceInterpretation:
        normalized_evidence_type = evidence_type.strip().lower()

        interpreter = self._interpreters.get(
            normalized_evidence_type
        )

        if interpreter is None:
            raise ValueError(
                f"Tipo de evidência não suportado: {evidence_type}"
            )

        return interpreter(value)

    def _interpret_simulado(
        self,
        value: str,
    ) -> EvidenceInterpretation:
        percentage = self._extract_percentage(value)

        status = classify_level(percentage)

        interpretation = self._build_interpretation(
            percentage=percentage,
            status=status,
        )

        return EvidenceInterpretation(
            discipline="desempenho",
            metric=SUPPORTED_METRIC,
            value=percentage,
            unit="percent",
            status=status,
            interpretation=interpretation,
        )

    # Padrões aceitos, nesta ordem de tentativa:
    #   1. "72%", "72 %", "72,5%", "72.5%"
    #   2. "72 por cento", "72,5 por cento" (com variação de espaços/caixa)
    _PERCENT_SYMBOL_PATTERN = re.compile(
        r"(\d+(?:[.,]\d+)?)\s*%"
    )

    _PERCENT_WORD_PATTERN = re.compile(
        r"(\d+(?:[.,]\d+)?)\s*por\s+cento",
        re.IGNORECASE,
    )

    @classmethod
    def _extract_percentage(cls, value: str) -> float:
        match = cls._PERCENT_SYMBOL_PATTERN.search(value)

        if match is None:
            match = cls._PERCENT_WORD_PATTERN.search(value)

        if not match:
            raise ValueError(
                "Não foi possível identificar um percentual "
                "na evidência."
            )

        return float(
            match.group(1).replace(",", ".")
        )

    @staticmethod
    def _build_interpretation(
        percentage: float,
        status: str,
    ) -> str:
        interpretations = {
            "critico": (
                f"Desempenho de {percentage:.1f}% de acerto. "
                "O resultado indica necessidade de "
                "intervenção prioritária."
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