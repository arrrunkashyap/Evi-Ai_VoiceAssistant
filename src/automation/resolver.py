"""Natural-language command resolver for EVI desktop automation.

This module intentionally stays deterministic for common desktop actions.
The AI providers can be used later for harder/ambiguous requests, but basic
computer control should not depend on Gemini or Ollama.
"""

from dataclasses import dataclass
import re
from typing import Optional


APP_ALIASES = {
    "chrome": ["google chrome", "chrome", "browser"],
    "edge": ["microsoft edge", "edge"],
    "firefox": ["mozilla firefox", "firefox"],
    "vscode": ["visual studio code", "vs code", "vscode", "code editor"],
    "notepad": ["notepad", "text editor"],
    "calculator": ["calculator", "calc"],
    "paint": ["paint", "microsoft paint"],
    "explorer": ["file explorer", "windows explorer", "explorer", "files"],
    "cmd": ["command prompt", "cmd"],
    "powershell": ["powershell", "power shell"],
    "taskmanager": ["task manager", "taskmgr"],
}


@dataclass(frozen=True)
class Intent:
    """A validated action EVI can execute locally."""

    name: str
    target: str
    confidence: float = 1.0


# Longer phrases are checked first so "google chrome" wins over "chrome".
_ALIASES = sorted(
    ((alias, app) for app, aliases in APP_ALIASES.items() for alias in aliases),
    key=lambda item: len(item[0]),
    reverse=True,
)

# Words that clearly express the requested action.
_ACTION_PATTERNS = {
    "close_app": [
        r"\bclose\b",
        r"\bquit\b",
        r"\bexit\b",
        r"\bshut\s+down\b",
        r"\bget\s+rid\s+of\b",
        r"\bget\s+.*\s+out\s+of\s+the\s+way\b",
    ],
    "open_app": [
        r"\bopen\b",
        r"\blaunch\b",
        r"\bstart\b",
        r"\brun\b",
        r"\bbring\s+up\b",
    ],
    "focus_app": [
        r"\bswitch\s+to\b",
        r"\bswitch\s+back\s+to\b",
        r"\bgo\s+to\b",
        r"\bfocus\s+(?:on\s+)?\b",
        r"\bbring\s+.*\s+to\s+the\s+front\b",
    ],
    "restart_app": [
        r"\brestart\b",
    ],
}

# Explicit negation should never become an executable action.
_NEGATION_PATTERNS = [
    r"\bdo\s+not\b",
    r"\bdon['’]?t\b",
    r"\bnever\b",
    r"\bplease\s+don['’]?t\b",
]


def _normalize(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9'’\s]", " ", text)
    return re.sub(r"\s+", " ", text)


def _find_target(text: str) -> Optional[str]:
    for alias, app in _ALIASES:
        if re.search(rf"(?<!\w){re.escape(alias)}(?!\w)", text):
            return app
    return None


def _find_action(text: str) -> Optional[str]:
    for intent, patterns in _ACTION_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text):
                return intent
    return None


def _is_negated(text: str) -> bool:
    return any(re.search(pattern, text) for pattern in _NEGATION_PATTERNS)


def resolve_command(user_text: str) -> Optional[Intent]:
    """Resolve a natural-language desktop request into a safe local intent.

    Returns None when the sentence is not an unambiguous desktop action.
    In particular, conversational questions and negated commands are left for
    the normal AI conversation path instead of executing anything.
    """

    raw_text = user_text.lower().strip()
    text = _normalize(raw_text)

    if not text or _is_negated(text):
        return None

    target = _find_target(text)
    if target is None:
        return None

    action = _find_action(text)
    if action is None:
        return None

    # Informational questions should not execute. Requests phrased as
    # "Can you open Chrome?" or "Could you close Chrome?" are valid commands.
    if raw_text.endswith("?") and re.match(
        r"^(what|why|is|are|does|do|did|where|when|which|who|how)\b",
        text,
    ):
        return None

    return Intent(name=action, target=target, confidence=0.95)


# Backwards-compatible helper used by older code/tests.
def resolve_app(user_text: str):
    """Return only the application target, if one is mentioned."""
    return _find_target(_normalize(user_text))
