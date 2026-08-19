import ctypes
import shutil
import subprocess
import psutil
from datetime import datetime


# ---------- Lock Computer ---------- #

def lock_pc():

    try:
        result = ctypes.windll.user32.LockWorkStation()

        if result:
            return "Locking your computer."

        return "Unable to lock computer."

    except Exception as e:
        return f"Unable to lock computer. ({e})"


# ---------- Shutdown ---------- #

def shutdown(delay: int = 5):

    try:
        subprocess.run(
            ["shutdown", "/s", "/t", str(delay)],
            check=True,
            capture_output=True,
            text=True
        )

        return f"Shutting down in {delay} seconds."

    except subprocess.CalledProcessError as e:
        error = e.stderr.strip() if e.stderr else "Windows command failed."
        return f"Shutdown failed. ({error})"

    except Exception as e:
        return f"Shutdown failed. ({e})"


# ---------- Restart ---------- #

def restart(delay: int = 5):

    try:
        subprocess.run(
            ["shutdown", "/r", "/t", str(delay)],
            check=True,
            capture_output=True,
            text=True
        )

        return f"Restarting in {delay} seconds."

    except subprocess.CalledProcessError as e:
        error = e.stderr.strip() if e.stderr else "Windows command failed."
        return f"Restart failed. ({error})"

    except Exception as e:
        return f"Restart failed. ({e})"


# ---------- Logout ---------- #

def logout():

    try:
        subprocess.run(
            ["shutdown", "/l"],
            check=True
        )

        return "Logging out."

    except Exception as e:
        return f"Logout failed. ({e})"


# ---------- Cancel Shutdown ---------- #

def cancel_shutdown():

    try:
        subprocess.run(
            ["shutdown", "/a"],
            check=True,
            capture_output=True,
            text=True
        )

        return "Shutdown cancelled."

    except subprocess.CalledProcessError:
        return "There is no pending shutdown to cancel."

    except Exception as e:
        return f"Unable to cancel shutdown. ({e})"


# ---------- Sleep ---------- #

def sleep():

    try:
        result = ctypes.windll.powrprof.SetSuspendState(
            False,  # Hibernate = False
            True,   # Force sleep
            False   # Disable wake events = False
        )

        if result:
            return "Putting computer to sleep."

        return "Unable to put computer to sleep."

    except Exception as e:
        return f"Sleep failed. ({e})"


# ---------- Hibernate ---------- #

def hibernate():

    try:
        subprocess.run(
            ["shutdown", "/h"],
            check=True,
            capture_output=True,
            text=True
        )

        return "Hibernating computer."

    except subprocess.CalledProcessError as e:
        error = e.stderr.strip() if e.stderr else "Windows command failed."
        return f"Hibernate failed. ({error})"

    except Exception as e:
        return f"Hibernate failed. ({e})"


# ---------- Empty Recycle Bin ---------- #

def empty_recycle_bin():

    try:
        subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "Clear-RecycleBin -Force"
            ],
            check=True,
            capture_output=True,
            text=True
        )

        return "Recycle Bin emptied."

    except Exception as e:
        return f"Unable to empty Recycle Bin. ({e})"


# ---------- CPU Usage ---------- #

def cpu_usage():

    return f"CPU usage is {psutil.cpu_percent(interval=1)} percent."


# ---------- RAM Usage ---------- #

def ram_usage():

    ram = psutil.virtual_memory()

    return (
        f"RAM usage is {ram.percent} percent. "
        f"{round(ram.used / (1024**3), 2)} GB used of "
        f"{round(ram.total / (1024**3), 2)} GB."
    )


# ---------- Disk Usage ---------- #

def disk_usage():

    disk = shutil.disk_usage("C:\\")

    used = round(disk.used / (1024**3), 2)
    total = round(disk.total / (1024**3), 2)
    percent = round((disk.used / disk.total) * 100, 1)

    return (
        f"Disk usage is {percent} percent. "
        f"{used} GB used of {total} GB."
    )


# ---------- System Uptime ---------- #

def uptime():

    boot = psutil.boot_time()
    boot_time = datetime.fromtimestamp(boot)

    return (
        f"System started at "
        f"{boot_time.strftime('%I:%M %p on %d %B %Y')}."
    )


# ---------- Battery ---------- #

def battery_status():

    battery = psutil.sensors_battery()

    if battery is None:
        return "Battery information is unavailable."

    status = "charging" if battery.power_plugged else "not charging"

    return (
        f"Battery is {battery.percent}% "
        f"and is currently {status}."
    )