import sys
import shutil
import argparse
from pathlib import Path


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Recursively copy files from a source directory and "
                    "sort them into subdirectories named after their extension."
    )
    parser.add_argument("source", help="path to the source directory")
    parser.add_argument(
        "destination",
        nargs="?",
        default="dist",
        help="path to the destination directory (default: dist)",
    )

    return parser.parse_args()


# Files with the same name can come from different subdirectories, and all of
# them land in the same folder. A numeric suffix keeps every one of them instead
# of letting the last copy overwrite the previous ones.
def resolve_name_conflict(target: Path) -> Path:
    counter = 1
    candidate = target

    while candidate.exists():
        candidate = target.with_name(f"{target.stem}_{counter}{target.suffix}")
        counter += 1

    return candidate


def copy_file(file_path: Path, destination: Path) -> None:
    extension = file_path.suffix.lstrip(".").lower() or "no_extension"
    target_dir = destination / extension

    try:
        target_dir.mkdir(parents=True, exist_ok=True)
        target = resolve_name_conflict(target_dir / file_path.name)
        shutil.copy2(file_path, target)
        print(f"Copied: {file_path.name} -> {extension}/{target.name}")
    except OSError as error:
        print(f"Cannot copy '{file_path}': {error}")


def process_directory(source: Path, destination: Path) -> None:
    try:
        items = list(source.iterdir())
    except OSError as error:
        print(f"Cannot read '{source}': {error}")
        return

    for item in items:
        if item.is_dir():
            process_directory(item, destination)
        elif item.is_file():
            copy_file(item, destination)


def main() -> None:
    args = parse_arguments()
    source = Path(args.source).resolve()
    destination = Path(args.destination).resolve()

    if not source.is_dir():
        print(f"Source directory does not exist: {source}")
        sys.exit(1)

    if destination == source or source in destination.parents:
        print("The destination directory must be located outside the source directory.")
        sys.exit(1)

    try:
        destination.mkdir(parents=True, exist_ok=True)
    except OSError as error:
        print(f"Cannot create the destination directory: {error}")
        sys.exit(1)

    print(f"Source:      {source}")
    print(f"Destination: {destination}\n")

    process_directory(source, destination)
    print(f"\nDone. All files have been sorted by extension in: {destination}")


main()
