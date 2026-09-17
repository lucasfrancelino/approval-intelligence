from typing import Literal


Direction = Literal[
    "evolucao",
    "queda",
    "estavel",
]

Status = Literal[
    "positivo",
    "negativo",
    "neutro",
]

Level = Literal[
    "critico",
    "atencao",
    "bom",
    "excelente",
]


def classify_direction(variation: float) -> Direction:
    if variation > 0:
        return "evolucao"

    if variation < 0:
        return "queda"

    return "estavel"


def classify_status(direction: str) -> Status:
    if direction == "evolucao":
        return "positivo"

    if direction == "queda":
        return "negativo"

    return "neutro"


def classify_level(value: float) -> Level:
    if value < 50:
        return "critico"

    if value < 70:
        return "atencao"

    if value < 85:
        return "bom"

    return "excelente"