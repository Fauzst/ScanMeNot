"""Data models shared by the SentinelScan collectors."""

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class OSInfo:
    """Operating system details reported by the platform module."""

    system: str
    release: str
    version: str
    architecture: Tuple[str, str]


@dataclass
class SystemInfo:
    """Basic information about the current endpoint."""

    hostname: str
    os: OSInfo


@dataclass
class ProcessInfo:
    """A single process observed during a scan."""

    pid: int
    name: Optional[str]
    exe: Optional[str]
    username: Optional[str]
    status: Optional[str]
    cpu_percent: Optional[float]
    memory_rss: Optional[int]
    create_time: Optional[float]
