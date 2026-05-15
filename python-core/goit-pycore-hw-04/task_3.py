import sys
from pathlib import Path
from colorama import init, Fore, Style

init(autoreset=True)

def visualize_directory(path: Path, indent: str = "") -> None:
    entries = sorted(path.iterdir(), key=lambda e: (e.is_file(), e.name))
    for i, entry in enumerate(entries):
        connector = "└── " if i == len(entries) - 1 else "├── "
        if entry.is_dir():
            print(f"{indent}{connector}{Fore.CYAN}{Style.BRIGHT}{entry.name}/")
            extension = "    " if i == len(entries) - 1 else "│   "
            visualize_directory(entry, indent + extension)
        else:
            print(f"{indent}{connector}{Fore.GREEN}{entry.name}")


def main() -> None:
    if len(sys.argv) != 2:
        print(f"{Fore.RED}Usage: python task_3.py <path_to_directory>")
        sys.exit(1)

    target = Path(sys.argv[1])

    if not target.exists():
        print(f"{Fore.RED}Path does not exist: {target}")
        sys.exit(1)

    if not target.is_dir():
        print(f"{Fore.RED}Not a directory: {target}")
        sys.exit(1)

    print(f"{Fore.CYAN}{Style.BRIGHT}{target.name}/")
    visualize_directory(target)

# Let's Test!
main()