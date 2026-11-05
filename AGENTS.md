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
- `src/collectors/models.py` defines dataclasses (`OSInfo`, `SystemInfo`, `ProcessInfo`). Collectors return dataclass instances, not dicts.
- `src/main.py` is a minimal CLI that prints the process snapshot; it is not yet the full scanner entrypoint.
- `src/collectors/system.py` is side-effect free on import; keep it that way (no module-level execution or printing).
- `src/collectors/processes.py` uses `psutil` to return `list[ProcessInfo]` sorted by PID. Inaccessible processes are skipped; missing fields stay `None`.
- `src/installers/*.ps1` are Windows setup/bootstrap scripts (NuGet, WinGet), not part of the Python package or the pytest run.
- Windows security collectors will require admin rights and must handle unavailable/unsupported features gracefully. Expect platform-dependent behavior.

## Commands (run from repo root)

- Install dependencies first: `python -m pip install -r requirements.txt`
- `pytest` is **not** on PATH; use `python -m pytest`.
- All tests: `python -m pytest`
- One file: `python -m pytest test/test_processes.py -q`
- One test: `python -m pytest test/test_processes.py::test_collect_processes_works_against_the_real_system -q`
- Run the CLI: `python src\main.py` (or `python -m collectors.processes` from `src` on `PYTHONPATH`).

## Testing notes

- `pytest.ini` sets `pythonpath = src`, so tests import `from collectors.system import collect_sysinfo`. Always run from the repo root; running from inside `test/` breaks imports.
- Tests live in `test/` (singular), not `tests/`; files must match `test_*.py`.
- Current baseline (verify before relying on it): `python -m pytest` gives **21 passed, 2 xfailed**. The 2 strict xfails cover hardware and uptime collection, which are not implemented yet (TODO 2.1). When implementing them, convert the xfails into real tests.
- Do not "fix" failing tests by editing `src/`; align the tests or propose the contract change to the human.
- Dependencies are declared in `requirements.txt` (`psutil` runtime, `pytest` for tests). There is no CI yet.
