"""Collect information about running processes on the local machine."""

from typing import Optional

import psutil

from .models import ProcessInfo

_PROCESS_ATTRS = (
    "pid",
    "name",
    "exe",
    "username",
    "status",
    "cpu_percent",
    "memory_info",
    "create_time",
)


def _memory_rss(memory_info) -> Optional[int]:
    """Return resident memory in bytes, or None when it is unavailable."""
    if memory_info is None:
        return None
    return getattr(memory_info, "rss", None)


def collect_processes() -> list[ProcessInfo]:
    """Return a read-only snapshot of running processes, sorted by PID.

    CPU percent is 0.0 on the first scan for a given process. Protected
    processes may return None for fields the current user cannot access;
    inaccessible processes are skipped rather than aborting the scan.
    """
    processes: list[ProcessInfo] = []

    try:
        pids = psutil.pids()
    except psutil.Error:
        return processes

    for pid in pids:
        try:
            process = psutil.Process(pid)
            with process.oneshot():
                info = process.as_dict(attrs=_PROCESS_ATTRS, ad_value=None)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

        processes.append(
            ProcessInfo(
                pid=info["pid"],
                name=info.get("name"),
                exe=info.get("exe"),
                username=info.get("username"),
                status=info.get("status"),
                cpu_percent=info.get("cpu_percent"),
                memory_rss=_memory_rss(info.get("memory_info")),
                create_time=info.get("create_time"),
            )
        )

    return sorted(processes, key=lambda process: process.pid)
