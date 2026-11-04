import json
import os
import subprocess
import sys
from dataclasses import asdict
from pathlib import Path

from collectors.system import collect_sysinfo

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_collector_output_is_json_serializable():
    info = collect_sysinfo()
    payload = asdict(info)

    serialized = json.dumps(payload)
    restored = json.loads(serialized)

    assert isinstance(restored, dict)
    assert set(restored) == {"hostname", "os"}
    assert set(restored["os"]) == {"system", "release", "version", "architecture"}
    assert restored["hostname"] == info.hostname
    assert restored["os"]["system"] == info.os.system


def test_collector_works_in_a_fresh_interpreter():
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from collectors.system import collect_sysinfo; "
            "print(collect_sysinfo().hostname)",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        env={
            **os.environ,
            "PYTHONPATH": str(REPO_ROOT / "src"),
        },
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() != ""


def test_main_entrypoint_runs_without_error():
    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / "src" / "main.py")],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "Traceback" not in result.stderr
