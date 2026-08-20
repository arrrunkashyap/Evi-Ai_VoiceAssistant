import re


# ---------------------------------------------------------
# Workflow separators
# ---------------------------------------------------------

SEPARATORS = [
    r"\s+and then\s+",
    r"\s+then\s+",
    r"\s+after that\s+",
    r"\s*,\s*and\s+",
    r"\s+and\s+",
]


def split_workflow(command: str) -> list[str]:
    """
    Split a natural-language workflow into individual commands.

    Example:
        "open chrome and then open youtube"

    becomes:
        [
            "open chrome",
            "open youtube"
        ]
    """

    command = command.lower().strip()

    if not command:
        return []

    parts = [command]

    for separator in SEPARATORS:
        new_parts = []

        for part in parts:
            new_parts.extend(
                re.split(separator, part)
            )

        parts = new_parts

    return [
        part.strip(" ,.")
        for part in parts
        if part.strip(" ,.")
    ]


def is_workflow(command: str) -> bool:
    """
    Determine whether a command contains multiple actions.
    """

    parts = split_workflow(command)

    return len(parts) > 1