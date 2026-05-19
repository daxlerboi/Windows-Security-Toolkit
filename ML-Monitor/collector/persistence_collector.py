import winreg
import os
import subprocess

RUN_KEYS = [
    (
        winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Run"
    ),
    (
        winreg.HKEY_LOCAL_MACHINE,
        r"Software\Microsoft\Windows\CurrentVersion\Run"
    )
]

STARTUP_FOLDER = os.path.expandvars(
    r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
)

def collect_registry_persistence():

    entries = []

    for root, path in RUN_KEYS:

        try:

            key = winreg.OpenKey(root, path)

            i = 0

            while True:

                try:

                    name, value, _ = winreg.EnumValue(key, i)

                    entries.append({
                        "type": "registry",
                        "name": name,
                        "command": value,
                        "location": path
                    })

                    i += 1

                except OSError:
                    break

        except:
            continue

    return entries

def collect_startup_folder():

    entries = []

    try:

        for file in os.listdir(STARTUP_FOLDER):

            full_path = os.path.join(
                STARTUP_FOLDER,
                file
            )

            entries.append({
                "type": "startup",
                "name": file,
                "command": full_path,
                "location": STARTUP_FOLDER
            })

    except:
        pass

    return entries

def collect_scheduled_tasks():

    tasks = []

    try:

        output = subprocess.check_output(
            "schtasks /query /fo LIST /v",
            shell=True,
            text=True
        )

        tasks.append({
            "type": "scheduled_task",
            "output": output
        })

    except:
        pass

    return tasks

def collect_persistence():

    data = []

    data.extend(
        collect_registry_persistence()
    )

    data.extend(
        collect_startup_folder()
    )

    return data