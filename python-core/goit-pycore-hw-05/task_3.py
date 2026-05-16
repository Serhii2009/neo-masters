import sys
from pathlib import Path
from collections import defaultdict

def parse_log_line(line: str) -> dict:
    parts = line.strip().split(" ", 3)
    return {
        "date": parts[0],
        "time": parts[1],
        "level": parts[2],
        "message": parts[3] if len(parts) > 3 else "",
    }

def load_logs(file_path: str) -> list:
    path = Path(__file__).parent / file_path

    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        sys.exit(1)
    except Exception as error:
        print(f"Error reading file: {error}")
        sys.exit(1)

    return [
        parse_log_line(line)
        for line in lines
        if line.strip()
    ]

def filter_logs_by_level(logs: list, level: str) -> list:
    return list(
        filter(
            lambda log: log["level"].upper() == level.upper(),
            logs
        )
    )

def count_logs_by_level(logs: list) -> dict:
    counts = defaultdict(int)

    for log in logs:
        counts[log["level"]] += 1
    return dict(counts)

def display_log_counts(counts: dict) -> None:
    print(f"\n{'Log Level':<17}| Count")
    print(f"{'-' * 17}|----------")
    for level, count in sorted(counts.items()):
        print(f"{level:<17}| {count}")

def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python task_3.py <path_to_logfile> [level]")
        sys.exit(1)

    logs = load_logs(sys.argv[1])
    counts = count_logs_by_level(logs)
    display_log_counts(counts)

    if len(sys.argv) == 3:
        level = sys.argv[2].upper()
        filtered_logs = filter_logs_by_level(logs, level)
        print(f"\nLog details for level '{level}':")

        for log in filtered_logs:
            print(
                f"{log['date']} "
                f"{log['time']} - "
                f"{log['message']}"
            )

main()