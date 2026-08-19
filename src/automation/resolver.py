"""Local natural-language command resolver for EVI.

This module converts common natural-language desktop requests into a small,
validated intent structure. It deliberately does not execute anything.
"""

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
    "explorer": ["file explorer", "windows explorer", "explorer"],
    "cmd": ["command prompt", "cmd"],
    "powershell": ["power shell", "powershell"],
    "taskmanager": ["task manager", "taskmanager"],
}

WEBSITE_ALIASES = {
    "google": ["google"],
    "youtube": ["youtube"],
    "github": ["github"],
    "chatgpt": ["chatgpt", "chat gpt"],
    "linkedin": ["linkedin", "linked in"],
    "gmail": ["gmail", "google mail"],
    "leetcode": ["leetcode"],
    "stackoverflow": ["stack overflow", "stackoverflow"],
    "maps": ["google maps", "maps"],
}

FOLDER_ALIASES = {
    "downloads": ["downloads", "download folder"],
    "documents": ["documents", "documents folder", "docs folder"],
    "desktop": ["desktop", "desktop folder"],
    "pictures": ["pictures", "photos folder", "picture folder"],
    "music": ["music", "music folder"],
    "videos": ["videos", "video folder"],
    "thispc": ["this pc", "my computer", "computer"],
    "recyclebin": ["recycle bin", "trash", "trash bin"],
}

# Words that usually indicate a request is NOT an executable command.
NEGATION_PATTERNS = (
    r"\bdo not\b",
    r"\bdon't\b",
    r"\bdont\b",
    r"\bnever\b",
    r"\bnot\b",
)

OPEN_WORDS = ("open", "launch", "start", "run", "bring up", "load")
CLOSE_WORDS = ("close", "quit", "exit", "shut", "terminate", "get rid of", "get it out of the way", "get that out of the way", "finished with", "done with")
FOCUS_WORDS = ("switch to", "switch back to", "focus on", "bring me to", "go to")
RESTART_WORDS = ("restart", "relaunch")


def _contains(text: str, phrases) -> bool:
    return any(re.search(r"(?<!\w)" + re.escape(p) + r"(?!\w)", text) for p in phrases)


def _find_alias(text: str, aliases: dict) -> Optional[str]:
    # Longest alias first prevents "browser"-style broad aliases from winning
    # over a more specific phrase.
    candidates = []
    for canonical, values in aliases.items():
        for value in values:
            if _contains(text, [value]):
                candidates.append((len(value), canonical))
    return max(candidates)[1] if candidates else None


def _has_negation(text: str) -> bool:
    return any(re.search(pattern, text) for pattern in NEGATION_PATTERNS)


def _intent(intent: str, target: Optional[str] = None, **params):
    result = {"intent": intent, "target": target, "confidence": 0.95}
    result.update(params)
    return result


def resolve_command(user_text: str) -> Optional[dict]:
    """Resolve a common natural-language command without executing it."""
    if not user_text:
        return None

    text = re.sub(r"\s+", " ", user_text.lower().strip())

    if text in {"exit", "bye", "stop", "goodbye", "quit"}:
        return _intent("exit", confidence=1.0)

    # Never execute a destructive/local command when the sentence is clearly
    # negated. The conversation/AI layer can handle the sentence instead.
    if _has_negation(text):
        return None

    # Search commands are handled before generic website opening.
    search_match = re.match(r"^(?:please\s+)?search\s+(google|youtube|github|maps)\s+(.+)$", text)
    if search_match:
        return _intent("search", search_match.group(1), query=search_match.group(2), confidence=0.98)

    wiki_match = re.match(r"^(?:please\s+)?(?:search\s+)?wikipedia\s+(?:for\s+)?(.+)$", text)
    if wiki_match:
        return _intent("search_wikipedia", "wikipedia", query=wiki_match.group(1), confidence=0.98)

    app = _find_alias(text, APP_ALIASES)
    if app:
        if _contains(text, RESTART_WORDS):
            return _intent("restart_app", app)
        if _contains(text, CLOSE_WORDS):
            return _intent("close_app", app)
        if _contains(text, FOCUS_WORDS):
            return _intent("focus_app", app)
        if _contains(text, OPEN_WORDS):
            return _intent("open_app", app)

    website = _find_alias(text, WEBSITE_ALIASES)
    if website and _contains(text, OPEN_WORDS + FOCUS_WORDS):
        return _intent("open_website", website)

    folder = _find_alias(text, FOLDER_ALIASES)
    if folder and _contains(text, OPEN_WORDS):
        return _intent("open_folder", folder)

    # System actions. Use action phrases rather than matching words such as
    # "shutdown" anywhere in an unrelated sentence.
    if _contains(text, ("cancel shutdown", "cancel the shutdown", "abort shutdown")):
        return _intent("cancel_shutdown")
    if _contains(text, ("shut down", "shutdown", "turn off my pc", "turn off the computer")):
        return _intent("shutdown")
    if _contains(text, ("restart my pc", "restart the computer", "restart computer", "reboot my pc", "reboot the computer")):
        return _intent("restart")
    if _contains(text, ("lock my pc", "lock the computer", "lock computer", "lock my computer")):
        return _intent("lock")
    if _contains(text, ("put my pc to sleep", "put my computer to sleep", "put the computer to sleep", "sleep my pc", "sleep my computer", "sleep the computer")):
        return _intent("sleep")
    if _contains(text, ("hibernate my pc", "hibernate the computer", "hibernate computer")):
        return _intent("hibernate")
    if _contains(text, ("log me out", "log out", "logout")):
        return _intent("logout")

    # Information commands.
    info_phrases = {
        "battery": ("battery status", "battery percentage", "how much battery", "battery level"),
        "cpu": ("cpu usage", "processor usage", "cpu utilization"),
        "ram": ("ram usage", "memory usage", "how much ram"),
        "disk": ("disk usage", "storage usage", "disk space"),
        "uptime": ("system uptime", "how long has the computer been on"),
        "time": ("what time is it", "current time", "tell me the time"),
        "date": ("what is today's date", "what's today's date", "current date", "today's date"),
        "day": ("what day is it", "what day is today", "today's day"),
        "month": ("what month is it", "current month"),
        "year": ("what year is it", "current year"),
    }
    for intent, phrases in info_phrases.items():
        if _contains(text, phrases):
            return _intent(intent)

    return None


# Backward-compatible helper used by older code.
def resolve_app(user_text: str):
    result = resolve_command(user_text)
    if result and result.get("target") in APP_ALIASES:
        return result["target"]
    return _find_alias(user_text.lower(), APP_ALIASES)
