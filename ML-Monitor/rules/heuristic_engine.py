from rules.suspicious_paths import (
    SUSPICIOUS_PATHS
)
# Imports the SUSPICIOUS_PATHS list (like "temp" or "appdata") from a separate, custom file named
#  'suspicious_paths' located in a 'rules' folder. 
# This keeps the main code clean and allows you to update the list of bad paths in just one place.

def calculate_risk(process):
# Defines a new function named calculate_risk to evaluate how
#  dangerous a currently running process might be.

    score = 0
    # Initializes a risk score starting at 0. 
    # We will add points to this score as we find suspicious behaviors.

    exe_path = str(
        process.get("exe", "")
    ).lower()
    # Safely retrieves the file path ('exe') from the process data. 
    # The '.get("exe", "")' part ensures the script doesn't crash 
    # if the path is missing (it just defaults to an empty text string).
    # It then converts it all to lowercase.

    process_name = str(
        process.get("name", "")
    ).lower()
    # Safely retrieves the name of the process (like "chrome.exe") and converts it to lowercase.

    cpu = process.get("cpu", 0)
    memory = process.get("memory", 0)
    # Safely retrieves the CPU and memory usage numbers. 
    # If the data is missing, it defaults to 0 so the math later on doesn't break.

    for path in SUSPICIOUS_PATHS:
        if path in exe_path:
            score += 5
    # Loops through our imported list of bad folders. 
    # If the program is running from one of those folders, it adds 5 points to the risk score.

    if cpu > 80:
        score += 3
    # If the process is using more than 80% of the computer's CPU, 
    # it adds 3 points. High CPU usage can indicate crypto-mining or ransomware encrypting files.

    if memory > 30:
        score += 3
    # If the process is using more than 30% of the total system memory (RAM), it adds 3 points.

    suspicious_names = [
        "powershell.exe",
        "cmd.exe",
        "wscript.exe",
        "cscript.exe"
    ]
    # Creates a short list of legitimate Windows administration tools. Hackers frequently hijack these tools to run malicious scripts without needing to install new viruses.

    if process_name in suspicious_names:
        score += 2
    # If the program running is one of those highly-abused Windows tools, 
    # it adds 2 points to the risk score.

    return score
    # Sends the final calculated score for this
    # running process back to wherever the function was called.

def persistence_risk(entry):
# Defines a second function named persistence_risk. T
# his one is specifically for evaluating the startup programs (persistence) 
# we found in the registry script earlier.

    score = 0
    # Starts a fresh risk score at 0 for this startup entry.

    command = str(
        entry.get("command", "")
    ).lower()
    # Safely retrieves the exact command or file path the registry uses to 
    # launch the program at startup, converting it to lowercase.

    for path in SUSPICIOUS_PATHS:
        if path in command:
            score += 5
    # Just like the running processes, if a program is scheduled to start 
    # automatically from a folder like 'temp', it gets a heavy penalty of 5 points.

    if "powershell" in command:
        score += 8
    # PowerShell starting automatically the moment you log into Windows is a massive red flag, 
    # so this adds 8 points. 

    if "cmd.exe" in command:
        score += 5
    # The Command Prompt starting silently in the background at login is also highly suspicious, 
    # adding 5 points.

    return score
    # Sends the final calculated risk score for this startup entry back to the main program.