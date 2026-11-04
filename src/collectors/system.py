import platform
from models import OSInfo, SystemInfo

def collect_sysinfo() -> SystemInfo:
    os_data = OSInfo(
        system=platform.system(),
        release=platform.release(),
        version=platform.version(),
        architecture=platform.architecture()
    )

    return SystemInfo(
        hostname=platform.node(),
        os=os_data
    )

print(collect_sysinfo())