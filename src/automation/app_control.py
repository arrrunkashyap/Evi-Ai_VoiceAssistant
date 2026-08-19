import subprocess
import psutil
import os
import shutil

import pygetwindow as gw


# --------------------------
# Application Registry
# --------------------------

APP_MAP = {
    "chrome": {
        "exe": "chrome.exe",
        "command": "chrome",
        "paths": [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ],
    },
    "edge": {
        "exe": "msedge.exe",
        "command": "msedge",
        "paths": [
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        ],
    },
    "firefox": {
        "exe": "firefox.exe",
        "command": "firefox",
        "paths": [
            r"C:\Program Files\Mozilla Firefox\firefox.exe",
            r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe",
        ],
    },
    "vscode": {
        "exe": "Code.exe",
        "command": "code",
        "paths": [
            os.path.expandvars(r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe"),
            r"C:\Program Files\Microsoft VS Code\Code.exe",
        ],
    },
    "notepad": {
        "exe": "notepad.exe",
        "command": "notepad",
        "paths": [],
    },
    "calculator": {
        "exe": "CalculatorApp.exe",
        "command": "calc",
        "paths": [],
    },
    "cmd": {
        "exe": "cmd.exe",
        "command": "cmd",
        "paths": [],
    },
    "powershell": {
        "exe": "powershell.exe",
        "command": "powershell",
        "paths": [],
    },
    "paint": {
        "exe": "mspaint.exe",
        "command": "mspaint",
        "paths": [],
    },
    "taskmanager": {
        "exe": "Taskmgr.exe",
        "command": "taskmgr",
        "paths": [],
    },
    "explorer": {
        "exe": "explorer.exe",
        "command": "explorer",
        "paths": [],
    },
}

def is_running(app_name: str) -> bool:

    app = APP_MAP.get(app_name.lower())

    if not app:
        return False

    exe = app["exe"].lower()

    for process in psutil.process_iter(["name"]):

        try:
            if process.info["name"] and process.info["name"].lower() == exe:
                return True
        except Exception:
            pass

    return False

def focus_window(app_name: str) -> bool:

    keywords = [
        app_name.lower()
    ]

    for window in gw.getAllTitles():

        if any(k in window.lower() for k in keywords):

            try:
                w = gw.getWindowsWithTitle(window)[0]

                if w.isMinimized:
                    w.restore()

                w.activate()

                return True

            except Exception:
                pass

    return False


def open_app(app_name: str):

    app_name = app_name.lower()

    if app_name not in APP_MAP:
        return False, f"I don't know how to open {app_name}."

    if focus_window(app_name):
        return True, f"{app_name} is already open."

    command = APP_MAP[app_name]["command"]

    try:
        # Prefer known Windows installation paths for applications such as
        # Chrome/Edge/Firefox/VS Code, then fall back to PATH.
        for path in APP_MAP[app_name].get("paths", []):
            if path and os.path.exists(path):
                subprocess.Popen([path])
                return True, f"Opening {app_name}."

        executable = shutil.which(command)
        if executable:
            subprocess.Popen([executable])
            return True, f"Opening {app_name}."

        return False, f"{app_name} is not installed."

    except Exception as e:
        return False, str(e)


def restart_app(app_name: str):
    """Restart a registered application."""
    closed, _ = close_app(app_name)
    if not closed and not is_running(app_name):
        # It is okay if the app was already closed; continue to opening it.
        pass
    return open_app(app_name)


def close_app(app_name: str):

    app = APP_MAP.get(app_name.lower())

    if not app:
        return False, "Unknown application."

    exe = app["exe"].lower()

    closed = False

    for process in psutil.process_iter(["pid", "name"]):

        try:

            if process.info["name"] and process.info["name"].lower() == exe:

                process.kill()

                closed = True

        except Exception:
            pass

    if closed:
        return True, f"{app_name} closed."

    return False, f"{app_name} isn't running."  