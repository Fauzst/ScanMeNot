import json
import os
from contextlib import nullcontext
from dataclasses import asdict
from types import SimpleNamespace

import psutil
import pytest

from collectors.models import ProcessInfo
from collectors.processes import collect_processes


class FakeProcess:
    def __init__(self, pid, info=None, error=None):
        self.pid = pid
        self._info = info or {}
        self._error = error

    def oneshot(self):
        return nullcontext()

    def as_dict(self, attrs=None, ad_value=None):
        if self._error is not None:
            raise self._error
        return {"pid": self.pid, **self._info}


def install_fakes(monkeypatch, processes_by_pid):
    monkeypatch.setattr(
        "collectors.processes.psutil.pids", lambda: list(processes_by_pid)
    )
    monkeypatch.setattr(
        "collectors.processes.psutil.Process", lambda pid: processes_by_pid[pid]
    )


def test_collect_processes_maps_psutil_fields(monkeypatch):
    memory_info = SimpleNamespace(rss=2048)
    fake = FakeProcess(
        42,
        {
            "name": "demo.exe",
            "exe": r"C:\demo.exe",
            "username": "DOMAIN\\user",
            "status": "running",
            "cpu_percent": 1.5,
            "memory_info": memory_info,
            "create_time": 123.0,
        },
    )
    install_fakes(monkeypatch, {42: fake})

    result = collect_processes()

    assert result == [
        ProcessInfo(
            pid=42,
            name="demo.exe",
            exe=r"C:\demo.exe",
            username="DOMAIN\\user",
            status="running",
            cpu_percent=1.5,
            memory_rss=2048,
            create_time=123.0,
        )
    ]


def test_collect_processes_returns_none_for_missing_fields(monkeypatch):
    install_fakes(monkeypatch, {7: FakeProcess(7, {"name": "partial.exe"})})

    result = collect_processes()

    assert result == [
        ProcessInfo(
            pid=7,
            name="partial.exe",
            exe=None,
            username=None,
            status=None,
            cpu_percent=None,
            memory_rss=None,
            create_time=None,
        )
    ]


@pytest.mark.parametrize(
    "error_type", [psutil.AccessDenied, psutil.NoSuchProcess, psutil.ZombieProcess]
)
def test_collect_processes_skips_inaccessible_processes(monkeypatch, error_type):
    install_fakes(monkeypatch, {9: FakeProcess(9, error=error_type(pid=9))})

    assert collect_processes() == []


def test_collect_processes_skips_process_that_disappears_before_lookup(monkeypatch):
    monkeypatch.setattr("collectors.processes.psutil.pids", lambda: [11])

    def fail(pid):
        raise psutil.NoSuchProcess(pid=pid)

    monkeypatch.setattr("collectors.processes.psutil.Process", fail)

    assert collect_processes() == []


def test_collect_processes_returns_empty_list_when_pids_fails(monkeypatch):
    def fail():
        raise psutil.Error("cannot enumerate processes")

    monkeypatch.setattr("collectors.processes.psutil.pids", fail)

    assert collect_processes() == []


def test_collect_processes_is_sorted_by_pid(monkeypatch):
    install_fakes(
        monkeypatch,
        {
            300: FakeProcess(300, {"name": "c.exe"}),
            100: FakeProcess(100, {"name": "a.exe"}),
            200: FakeProcess(200, {"name": "b.exe"}),
        },
    )

    assert [process.pid for process in collect_processes()] == [100, 200, 300]


def test_collect_processes_works_against_the_real_system():
    result = collect_processes()

    assert result
    assert all(isinstance(process, ProcessInfo) for process in result)

    pids = [process.pid for process in result]
    assert pids == sorted(pids)
    assert os.getpid() in pids


def test_collect_processes_output_is_json_serializable():
    payload = [asdict(process) for process in collect_processes()[:10]]

    json.dumps(payload)
