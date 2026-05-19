import psutil
import time

def collect_processes():

    process_data = []

    for proc in psutil.process_iter([
        'pid',
        'name',
        'memory_percent',
        'exe',
        'username'
    ]):

        try:

            proc.cpu_percent(interval=None)

            time.sleep(0.05)

            cpu = proc.cpu_percent(interval=None)

            process_info = {
                "pid": proc.info['pid'],
                "name": proc.info['name'],
                "cpu": cpu,
                "memory": round(
                    proc.info['memory_percent'],
                    2
                ),
                "exe": proc.info['exe'],
                "user": proc.info['username']
            }

            process_data.append(
                process_info
            )

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess
        ):
            continue

    return process_data