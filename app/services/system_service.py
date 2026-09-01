import platform

import psutil


def get_system_metrics():
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    return {
        "cpu": {
            "usage_percent": psutil.cpu_percent(interval=1),
            "cores": psutil.cpu_count()
        },
        "memory": {
            "total": memory.total,
            "used": memory.used,
            "available": memory.available,
            "usage_percent": memory.percent
        },
        "disk": {
            "total": disk.total,
            "used": disk.used,
            "free": disk.free,
            "usage_percent": disk.percent
        },
        "system": {
            "hostname": platform.node(),
            "operating_system": platform.system(),
            "platform": platform.platform()
        }
    }