class ActionStatus:
    RECOMMENDED = "recommended"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

    ALL = {
        RECOMMENDED,
        IN_PROGRESS,
        COMPLETED,
        CANCELLED,
    }

    ALLOWED_TRANSITIONS = {
        RECOMMENDED: {
            IN_PROGRESS,
            CANCELLED,
        },
        IN_PROGRESS: {
            COMPLETED,
            CANCELLED,
        },
        COMPLETED: set(),
        CANCELLED: set(),
    }


def validate_transition(
    current_status: str,
    new_status: str,
) -> None:
    if new_status not in ActionStatus.ALL:
        raise ValueError(
            f"Status inválido: {new_status}"
        )

    allowed_statuses = ActionStatus.ALLOWED_TRANSITIONS.get(
        current_status,
        set(),
    )

    if new_status not in allowed_statuses:
        raise ValueError(
            f"Transição não permitida: "
            f"{current_status} -> {new_status}"
        )