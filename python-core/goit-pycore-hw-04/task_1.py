from pathlib import Path

def total_salary(path: str) -> tuple[int, int]:
    try:
        file_path = Path(__file__).parent / path
        text = file_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"File not found: {path}")
        return 0, 0
    except Exception as e:
        print(f"Error reading file: {e}")
        return 0, 0

    salaries = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            _, salary = line.split(",")
            salaries.append(int(salary))
        except ValueError:
            print(f"Skipping malformed line: {line!r}")

    if not salaries:
        return 0, 0

    total = sum(salaries)
    average = total // len(salaries)
    return total, average

# Let's Test!
total, average = total_salary("salary_file.txt")
print(f"Загальна сума заробітної плати: {total}, Середня заробітна плата: {average}")