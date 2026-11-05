"""Minimal command-line entry point for the process collector."""

from collectors.processes import collect_processes


def main() -> None:
    """Print a read-only snapshot of running processes."""
    processes = collect_processes()
    print(f"{len(processes)} processes")
    print(f"{'PID':>6}  {'NAME':<30} {'RSS bytes':>12}")

    for process in processes:
        print(
            f"{process.pid:>6}  "
            f"{(process.name or '?'):<30} "
            f"{process.memory_rss or 0:>12}"
        )


if __name__ == "__main__":
    main()
