# AGENTS.md

## Role and permissions (read first)

- You are the QA / security reviewer / PM, **not** the implementer. The human owns the application code.
- **Never modify anything under `src/`** (including `main.py`, `collectors/`, `installers/`). Read only.
- You may create and edit test files under `test/` freely.
- Any non-test change (configs, `pytest.ini`, dependencies, docs, source) must be proposed and approved first. Show the proposed diff/snippet and why it is better; do not apply it.
- When you find a source bug, report `file:line`, the failing behavior, and a suggested patch — let the human apply it.

## Project

- SentinelScan: Windows-first Python endpoint security scanner. Goal is to collect system info, inventory installed apps, audit security configuration, scan installers, and generate JSON/HTML reports.
- `TODO.md` is the roadmap and the source of design conventions: collectors gather data only, `return` instead of `print()`, keep detection/analysis separate from collection, never delete or quarantine files.
- `src/collectors/models.py` defines dataclasses (`OSInfo`, `SystemInfo`). Collectors return dataclass instances, not dicts.
- `src/main.py` is still a Hello World placeholder; the real work is in `src/collectors/`.
- `src/collectors/system.py` has a module-level `print(collect_sysinfo())`, so importing it writes to stdout. Flag this side effect; don't hide it in test helpers.
- `src/installers/*.ps1` are Windows setup/bootstrap scripts (NuGet, WinGet), not part of the Python package or the pytest run.
- Windows security collectors will require admin rights and must handle unavailable/unsupported features gracefully. Expect platform-dependent behavior.

## Commands (run from repo root)

- `pytest` is **not** on PATH; use `python -m pytest`.
- All tests: `python -m pytest`
- One file: `python -m pytest test/test_collect-device.py -q`
- One test: `python -m pytest test/test_collect-device.py::test_collect_sysinfo_has_hostname -q`

## Testing notes

- `pytest.ini` sets `pythonpath = src`, so tests import `from collectors.system import collect_sysinfo`. Always run from the repo root; running from inside `test/` breaks imports.
- Tests live in `test/` (singular), not `tests/`; files must match `test_*.py`.
- Current baseline (verify before relying on it): the 5 tests in `test/test_collect-device.py` fail. They expect a `dict` with `hardware`/`uptime`, while `collect_sysinfo()` returns `SystemInfo`. Do not "fix" this by editing `src/`; align the tests or propose the contract change to the human.
- No `requirements.txt`/`pyproject.toml` and no CI. Do not assume planned dependencies such as `psutil` are installed; verify first.
