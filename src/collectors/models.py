from dataclasses import dataclass
from typing import Tuple

@dataclass
class OSInfo:
    system: str
    release: str
    version: str
    architecture: Tuple[str, str]

@dataclass
class SystemInfo:
    hostname: str
    os: OSInfo