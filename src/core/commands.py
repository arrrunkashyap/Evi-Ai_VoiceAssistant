from src.commands.apps import *
from src.commands.browser import *
from src.commands.files import *
from src.commands.system import *
from src.commands.datetime_cmd import *
from src.automation.resolver import resolve_command
from src.automation.app_control import open_app, close_app, focus_window


# ---------------- Command Lists ---------------- #

COMMANDS = {

    # ---------- Apps ---------- #

    "chrome": [
        "open chrome",
        "launch chrome",
        "start chrome",
        "open browser"
    ],

    "edge": [
        "open edge"
    ],

    "firefox": [
        "open firefox"
    ],

    "vscode": [
        "open vscode",
        "open visual studio code",
        "launch vscode"
    ],

    "notepad": [
        "open notepad"
    ],

    "calculator": [
        "open calculator",
        "open calc"
    ],

    "paint": [
        "open paint"
    ],

    "explorer": [
        "open explorer",
        "open file explorer"
    ],

    "cmd": [
        "open cmd",
        "open command prompt"
    ],

    "powershell": [
        "open powershell"
    ],

    "taskmanager": [
        "open task manager"
    ],

    # ---------- Browser ---------- #

    "google": [
        "open google"
    ],

    "youtube": [
        "open youtube"
    ],

    "github": [
        "open github"
    ],

    "chatgpt": [
        "open chatgpt"
    ],

    "linkedin": [
        "open linkedin"
    ],

    "gmail": [
        "open gmail"
    ],

    "leetcode": [
        "open leetcode"
    ],

    "stackoverflow": [
        "open stack overflow"
    ],

    # ---------- Files ---------- #

    "downloads": [
        "open downloads"
    ],

    "documents": [
        "open documents"
    ],

    "desktop": [
        "open desktop"
    ],

    "pictures": [
        "open pictures"
    ],

    "music": [
        "open music"
    ],

    "videos": [
        "open videos"
    ],

    "thispc": [
        "open this pc"
    ],

    "recyclebin": [
        "open recycle bin"
    ],

    # ---------- System ---------- #

    "shutdown": [
        "shutdown computer",
        "shutdown pc",
        "shut down"
    ],

    "restart": [
        "restart computer",
        "restart pc"
    ],

    "lock": [
        "lock computer",
        "lock pc"
    ],

    "sleep": [
        "sleep computer",
        "sleep pc"
    ],

    "hibernate": [
        "hibernate computer"
    ],

    "logout": [
        "logout",
        "log out"
    ],

    "cancelshutdown": [
        "cancel shutdown"
    ],

    "battery": [
        "battery status",
        "battery percentage"
    ],

    "cpu": [
        "cpu usage"
    ],

    "ram": [
        "ram usage",
        "memory usage"
    ],

    "disk": [
        "disk usage"
    ],

    "uptime": [
        "system uptime"
    ],

    # ---------- Date & Time ---------- #

    "time": [
        "what time",
        "current time",
        "time"
    ],

    "date": [
        "today date",
        "current date",
        "date"
    ],

    "day": [
        "today day",
        "day"
    ],

    "month": [
        "month"
    ],

    "year": [
        "year"
    ]
}


# ---------------- Execute ---------------- #

def execute_command(command: str):

    command = command.lower().strip()

    # ---------- Natural-language command bridge ---------- #
    # Resolve the user intent before falling back to the legacy command
    # phrases. The resolver never executes commands by itself.
    resolved = resolve_command(command)

    if resolved:
        intent = resolved["intent"]
        target = resolved.get("target")

        if intent == "exit":
            return "EXIT"

        if intent == "open_app":
            _, message = open_app(target)
            return message

        if intent == "close_app":
            _, message = close_app(target)
            return message

        if intent == "focus_app":
            if focus_window(target):
                return f"Switched to {target}."
            return f"I couldn't find an open {target} window."

        if intent == "restart_app":
            close_app(target)
            _, message = open_app(target)
            return f"Restarting {target}." if message else message

        if intent == "open_website":
            website_commands = {
                "google": open_google,
                "youtube": open_youtube,
                "github": open_github,
                "chatgpt": open_chatgpt,
                "linkedin": open_linkedin,
                "gmail": open_gmail,
                "leetcode": open_leetcode,
                "stackoverflow": open_stackoverflow,
                "maps": open_maps,
            }
            fn = website_commands.get(target)
            if fn:
                return fn()

        if intent == "open_folder":
            folder_commands = {
                "downloads": open_downloads,
                "documents": open_documents,
                "desktop": open_desktop,
                "pictures": open_pictures,
                "music": open_music,
                "videos": open_videos,
                "thispc": open_this_pc,
                "recyclebin": open_recycle_bin,
            }
            fn = folder_commands.get(target)
            if fn:
                return fn()

        if intent == "search":
            search_commands = {
                "google": search_google,
                "youtube": search_youtube,
                "github": search_github,
                "maps": search_maps,
            }
            fn = search_commands.get(target)
            if fn:
                return fn(resolved["query"])

        if intent == "search_wikipedia":
            return search_wikipedia(resolved["query"])

        system_commands = {
            "shutdown": shutdown,
            "restart": restart,
            "lock": lock_pc,
            "sleep": sleep,
            "hibernate": hibernate,
            "logout": logout,
            "cancel_shutdown": cancel_shutdown,
            "battery": battery_status,
            "cpu": cpu_usage,
            "ram": ram_usage,
            "disk": disk_usage,
            "uptime": uptime,
            "time": current_time,
            "date": current_date,
            "day": current_day,
            "month": current_month,
            "year": current_year,
        }
        fn = system_commands.get(intent)
        if fn:
            return fn()

    # Exit

    if command in ["exit", "bye", "stop", "goodbye"]:

        return "EXIT"

    # ---------- Apps ---------- #

    if any(c in command for c in COMMANDS["chrome"]):
        return open_chrome()

    if any(c in command for c in COMMANDS["edge"]):
        return open_edge()

    if any(c in command for c in COMMANDS["firefox"]):
        return open_firefox()

    if any(c in command for c in COMMANDS["vscode"]):
        return open_vscode()

    if any(c in command for c in COMMANDS["notepad"]):
        return open_notepad()

    if any(c in command for c in COMMANDS["calculator"]):
        return open_calculator()

    if any(c in command for c in COMMANDS["paint"]):
        return open_paint()

    if any(c in command for c in COMMANDS["explorer"]):
        return open_explorer()

    if any(c in command for c in COMMANDS["cmd"]):
        return open_cmd()

    if any(c in command for c in COMMANDS["powershell"]):
        return open_powershell()

    if any(c in command for c in COMMANDS["taskmanager"]):
        return open_task_manager()

    # ---------- Browser ---------- #

    if any(c in command for c in COMMANDS["google"]):
        return open_google()

    if any(c in command for c in COMMANDS["youtube"]):
        return open_youtube()

    if any(c in command for c in COMMANDS["github"]):
        return open_github()

    if any(c in command for c in COMMANDS["chatgpt"]):
        return open_chatgpt()

    if any(c in command for c in COMMANDS["linkedin"]):
        return open_linkedin()

    if any(c in command for c in COMMANDS["gmail"]):
        return open_gmail()

    if any(c in command for c in COMMANDS["leetcode"]):
        return open_leetcode()

    if any(c in command for c in COMMANDS["stackoverflow"]):
        return open_stackoverflow()

    # ---------- Search ---------- #

    if command.startswith("search google "):
        return search_google(command.replace("search google", "").strip())

    if command.startswith("search youtube "):
        return search_youtube(command.replace("search youtube", "").strip())

    if command.startswith("search github "):
        return search_github(command.replace("search github", "").strip())

    if command.startswith("search maps "):
        return search_maps(command.replace("search maps", "").strip())

    if command.startswith("wikipedia "):
        return search_wikipedia(command.replace("wikipedia", "").strip())

    # ---------- Files ---------- #

    if any(c in command for c in COMMANDS["downloads"]):
        return open_downloads()

    if any(c in command for c in COMMANDS["documents"]):
        return open_documents()

    if any(c in command for c in COMMANDS["desktop"]):
        return open_desktop()

    if any(c in command for c in COMMANDS["pictures"]):
        return open_pictures()

    if any(c in command for c in COMMANDS["music"]):
        return open_music()

    if any(c in command for c in COMMANDS["videos"]):
        return open_videos()

    if any(c in command for c in COMMANDS["thispc"]):
        return open_this_pc()

    if any(c in command for c in COMMANDS["recyclebin"]):
        return open_recycle_bin()

    # ---------- System ---------- #

    if any(c in command for c in COMMANDS["shutdown"]):
        return shutdown()

    if any(c in command for c in COMMANDS["restart"]):
        return restart()

    if any(c in command for c in COMMANDS["lock"]):
        return lock_pc()

    if any(c in command for c in COMMANDS["sleep"]):
        return sleep()

    if any(c in command for c in COMMANDS["hibernate"]):
        return hibernate()

    if any(c in command for c in COMMANDS["logout"]):
        return logout()

    if any(c in command for c in COMMANDS["cancelshutdown"]):
        return cancel_shutdown()

    if any(c in command for c in COMMANDS["battery"]):
        return battery_status()

    if any(c in command for c in COMMANDS["cpu"]):
        return cpu_usage()

    if any(c in command for c in COMMANDS["ram"]):
        return ram_usage()

    if any(c in command for c in COMMANDS["disk"]):
        return disk_usage()

    if any(c in command for c in COMMANDS["uptime"]):
        return uptime()

    # ---------- Date & Time ---------- #

    if any(c in command for c in COMMANDS["time"]):
        return current_time()

    if any(c in command for c in COMMANDS["date"]):
        return current_date()

    if any(c in command for c in COMMANDS["day"]):
        return current_day()

    if any(c in command for c in COMMANDS["month"]):
        return current_month()

    if any(c in command for c in COMMANDS["year"]):
        return current_year()

    return None