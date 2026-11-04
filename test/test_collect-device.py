import pytest

from collectors.models import OSInfo, SystemInfo
from collectors.system import collect_sysinfo


def test_collect_sysinfo_returns_system_info():
    assert isinstance(collect_sysinfo(), SystemInfo)


def test_collect_sysinfo_has_non_empty_hostname():
    info = collect_sysinfo()

    assert isinstance(info.hostname, str)
    assert info.hostname.strip() != ""


def test_collect_sysinfo_has_os_information():
    info = collect_sysinfo()

    assert isinstance(info.os, OSInfo)


@pytest.mark.parametrize("field", ["system", "release", "version"])
def test_os_text_fields_are_strings(field):
    os_info = collect_sysinfo().os

    assert isinstance(getattr(os_info, field), str)


def test_os_architecture_is_a_pair_of_strings():
    architecture = collect_sysinfo().os.architecture

    assert isinstance(architecture, tuple)
    assert len(architecture) == 2
    assert all(isinstance(part, str) for part in architecture)


def test_collect_sysinfo_maps_platform_values(monkeypatch):
    import collectors.system as system_module

    monkeypatch.setattr(system_module.platform, "system", lambda: "TestOS")
    monkeypatch.setattr(system_module.platform, "release", lambda: "1.2.3")
    monkeypatch.setattr(system_module.platform, "version", lambda: "build-42")
    monkeypatch.setattr(
        system_module.platform, "architecture", lambda: ("64bit", "TestPE")
    )
    monkeypatch.setattr(system_module.platform, "node", lambda: "test-host")

    assert collect_sysinfo() == SystemInfo(
        hostname="test-host",
        os=OSInfo(
            system="TestOS",
            release="1.2.3",
            version="build-42",
            architecture=("64bit", "TestPE"),
        ),
    )


@pytest.mark.xfail(
    reason="Hardware collection is not implemented in system.py yet (TODO 2.1)",
    strict=True,
)
def test_collect_sysinfo_has_hardware_information():
    info = collect_sysinfo()

    assert info.hardware.cpu_logical_cores > 0
    assert info.hardware.ram_total_bytes > 0
    assert 0 <= info.hardware.cpu_usage_percent <= 100
    assert 0 <= info.hardware.ram_usage_percent <= 100
    assert 0 <= info.hardware.disk_usage_percent <= 100


@pytest.mark.xfail(
    reason="Uptime/boot-time collection is not implemented in system.py yet (TODO 2.1)",
    strict=True,
)
def test_collect_sysinfo_has_uptime_information():
    info = collect_sysinfo()

    assert isinstance(info.uptime.boot_time, str)
