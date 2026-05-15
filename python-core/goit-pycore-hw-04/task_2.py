from pathlib import Path

def get_cats_info(path: str) -> list[dict]:
    try:
        file_path = Path(__file__).parent / path
        text = file_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"File not found: {path}")
        return []
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

    cats = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            cat_id, name, age = line.split(",")
            cats.append({"id": cat_id, "name": name, "age": age})
        except ValueError:
            print(f"Skipping malformed line: {line!r}")

    return cats

# Let's Test!
cats_info = get_cats_info("cats_file.txt")
for cat in cats_info:
    print(
        f"ID: {cat['id']}, "
        f"Name: {cat['name']}, "
        f"Age: {cat['age']}"
    )