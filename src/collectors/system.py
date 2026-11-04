import platform

def collect_sysinfo():
    sys_info = {
        "hostname" : platform.node(),
        "os": {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "architecture": platform.architecture()
        }
    }

    print(sys_info)

collect_sysinfo()