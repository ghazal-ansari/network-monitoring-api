import os
import platform

import psutil

from app.database.db import get_db


def _get_disk_root():
    if platform.system() == "Windows":
        return os.path.splitdrive(os.path.abspath(os.sep))[0] + "\\" or "C:\\"
    return "/"


def collect_metrics():
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage(_get_disk_root())

    network = psutil.net_io_counters()

    cpu_usage = psutil.cpu_percent(interval=0.5)
    memory_usage = memory.percent
    disk_usage = disk.percent

    bytes_sent = network.bytes_sent
    bytes_received = network.bytes_recv

    db = get_db()

    db.execute(
        """
        INSERT INTO monitoring_metrics (
            cpu_usage,
            memory_usage,
            disk_usage,
            bytes_sent,
            bytes_received
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            cpu_usage,
            memory_usage,
            disk_usage,
            bytes_sent,
            bytes_received
        )
    )

    db.commit()
    db.close()

    return {
        "cpu_usage": cpu_usage,
        "memory_usage": memory_usage,
        "disk_usage": disk_usage,
        "bytes_sent": bytes_sent,
        "bytes_received": bytes_received
    }