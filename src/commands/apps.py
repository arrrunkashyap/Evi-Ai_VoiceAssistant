import os
import shutil
import subprocess


def _open(executable: str, success: str, fail: str):
    try:
        if shutil.which(executable):
            subprocess.Popen([executable])
            return success

        return fail

    except Exception as e:
        return f"{fail} ({e})"


def _close(process_name: str, success: str, fail: str):
    try:
        result = subprocess.run(
            ["taskkill", "/IM", process_name, "/F"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            return success

        return fail

    except Exception as e:
        return f"{fail} ({e})"
# ---------------- Chrome ---------------- #

def open_chrome():

    chrome_paths = [

        r"C:\Program Files\Google\Chrome\Application\chrome.exe",

        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

    ]

    for path in chrome_paths:

        if os.path.exists(path):

            subprocess.Popen(path)

            return "Opening Google Chrome."

    return "Google Chrome is not installed."

def close_chrome():
    return _close(
        "chrome.exe",
        "Closing Google Chrome.",
        "Google Chrome is not running."
    )

# ---------------- Edge ---------------- #

def open_edge():

    edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

    if os.path.exists(edge):

        subprocess.Popen(edge)

        return "Opening Microsoft Edge."

    return "Microsoft Edge is not installed."


# ---------------- Firefox ---------------- #

def open_firefox():

    firefox = r"C:\Program Files\Mozilla Firefox\firefox.exe"

    if os.path.exists(firefox):

        subprocess.Popen(firefox)

        return "Opening Firefox."

    return "Firefox is not installed."


# ---------------- VS Code ---------------- #

def open_vscode():

    return _open(

        "code",

        "Opening Visual Studio Code.",

        "Visual Studio Code is not installed."

    )


# ---------------- Notepad ---------------- #

def open_notepad():

    return _open(

        "notepad",

        "Opening Notepad.",

        "Unable to open Notepad."

    )


# ---------------- Calculator ---------------- #

def open_calculator():

    return _open(

        "calc",

        "Opening Calculator.",

        "Unable to open Calculator."

    )


# ---------------- Paint ---------------- #

def open_paint():

    return _open(

        "mspaint",

        "Opening Paint.",

        "Unable to open Paint."

    )


# ---------------- Explorer ---------------- #

def open_explorer():

    return _open(

        "explorer",

        "Opening File Explorer.",

        "Unable to open File Explorer."

    )


# ---------------- CMD ---------------- #

def open_cmd():

    return _open(

        "cmd",

        "Opening Command Prompt.",

        "Unable to open Command Prompt."

    )


# ---------------- PowerShell ---------------- #

def open_powershell():

    return _open(

        "powershell",

        "Opening PowerShell.",

        "Unable to open PowerShell."

    )


# ---------------- Task Manager ---------------- #

def open_task_manager():

    return _open(

        "taskmgr",

        "Opening Task Manager.",

        "Unable to open Task Manager."

    )

# ---------------- WhatsApp ----------------

def open_whatsapp():

    try:
        # WhatsApp Desktop protocol
        os.startfile("whatsapp:")

        return "Opening WhatsApp."

    except Exception:
        pass

    # Common WhatsApp Desktop installation locations
    whatsapp_paths = [
        os.path.expandvars(
            r"%LOCALAPPDATA%\WhatsApp\WhatsApp.exe"
        ),
        os.path.expandvars(
            r"%LOCALAPPDATA%\Programs\WhatsApp\WhatsApp.exe"
        ),
        r"C:\Program Files\WhatsApp\WhatsApp.exe",
        r"C:\Program Files (x86)\WhatsApp\WhatsApp.exe"
    ]

    for path in whatsapp_paths:

        if os.path.exists(path):

            subprocess.Popen([path])

            return "Opening WhatsApp."

    return "WhatsApp is not installed."