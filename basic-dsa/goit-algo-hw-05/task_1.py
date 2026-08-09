import sys
import timeit
from pathlib import Path

ARTICLES = ["article_1.txt", "article_2.txt"]
ENCODINGS = ["utf-8", "cp1251"]
REPEATS = 50


def build_shift_table(pattern: str) -> dict:
    table = {}
    length = len(pattern)

    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1

    table.setdefault(pattern[-1], length)
    return table


def boyer_moore_search(text: str, pattern: str) -> int:
    if not pattern or len(pattern) > len(text):
        return -1

    shift_table = build_shift_table(pattern)
    position = 0

    while position <= len(text) - len(pattern):
        index = len(pattern) - 1

        while index >= 0 and text[position + index] == pattern[index]:
            index -= 1

        if index < 0:
            return position

        position += shift_table.get(text[position + len(pattern) - 1], len(pattern))

    return -1


def build_lps_table(pattern: str) -> list:
    lps = [0] * len(pattern)
    length = 0
    index = 1

    while index < len(pattern):
        if pattern[index] == pattern[length]:
            length += 1
            lps[index] = length
            index += 1
        elif length > 0:
            length = lps[length - 1]
        else:
            lps[index] = 0
            index += 1

    return lps


def knuth_morris_pratt_search(text: str, pattern: str) -> int:
    if not pattern or len(pattern) > len(text):
        return -1

    lps = build_lps_table(pattern)
    text_index = pattern_index = 0

    while text_index < len(text):
        if text[text_index] == pattern[pattern_index]:
            text_index += 1
            pattern_index += 1

            if pattern_index == len(pattern):
                return text_index - pattern_index
        elif pattern_index > 0:
            pattern_index = lps[pattern_index - 1]
        else:
            text_index += 1

    return -1


def polynomial_hash(text: str, base: int = 256, modulus: int = 101) -> int:
    hash_value = 0

    for char in text:
        hash_value = (hash_value * base + ord(char)) % modulus

    return hash_value


def rabin_karp_search(text: str, pattern: str) -> int:
    if not pattern or len(pattern) > len(text):
        return -1

    base = 256
    modulus = 101
    pattern_length = len(pattern)
    highest_power = pow(base, pattern_length - 1, modulus)

    pattern_hash = polynomial_hash(pattern, base, modulus)
    window_hash = polynomial_hash(text[:pattern_length], base, modulus)

    for position in range(len(text) - pattern_length + 1):
        if pattern_hash == window_hash:
            if text[position:position + pattern_length] == pattern:
                return position

        if position < len(text) - pattern_length:
            window_hash = (window_hash - ord(text[position]) * highest_power) % modulus
            window_hash = (window_hash * base + ord(text[position + pattern_length])) % modulus
            window_hash %= modulus

    return -1


ALGORITHMS = [
    ("Boyer-Moore", boyer_moore_search),
    ("Knuth-Morris-Pratt", knuth_morris_pratt_search),
    ("Rabin-Karp", rabin_karp_search),
]


def read_article(file_name: str) -> str:
    path = Path(__file__).parent / file_name

    for encoding in ENCODINGS:
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
        except OSError as error:
            print(f"Cannot read '{file_name}': {error}")
            sys.exit(1)

    print(f"Cannot decode '{file_name}' with any of: {', '.join(ENCODINGS)}")
    sys.exit(1)


def measure(algorithm, text: str, pattern: str) -> float:
    timer = timeit.Timer(lambda: algorithm(text, pattern))
    return timer.timeit(number=REPEATS) / REPEATS


def compare(title: str, text: str, patterns: list) -> dict:
    print(f"\n{title}: {len(text)} characters")

    width = max(len(label) for label, _ in patterns)
    header = f"{'Algorithm':<20}|" + "".join(f" {label:<{width}}|" for label, _ in patterns)
    print(header)
    print("-" * len(header))

    totals = {}

    for name, algorithm in ALGORITHMS:
        row = f"{name:<20}|"

        for _, pattern in patterns:
            elapsed = measure(algorithm, text, pattern)
            totals[name] = totals.get(name, 0) + elapsed
            row += f" {elapsed:<{width}.6f}|"

        print(row)

    fastest = min(totals, key=totals.get)
    print(f"Fastest for this text: {fastest} ({totals[fastest]:.6f} s in total)")
    return totals


def main() -> None:
    # Each existing pattern occurs exactly once and is located in the last third
    # of its article, so the algorithms have to scan most of the text.
    existing_patterns = [
        "оптимізаційних задач",
        "бінарних діаграм рішень",
    ]
    fake_pattern = "квантовий блокчейн даних"

    overall = {}

    for file_name, existing in zip(ARTICLES, existing_patterns):
        text = read_article(file_name)

        if existing not in text:
            print(f"Warning: the pattern '{existing}' was not found in {file_name}")

        patterns = [
            (f"existing: {existing}", existing),
            ("non-existing", fake_pattern),
        ]

        totals = compare(file_name, text, patterns)

        for name, value in totals.items():
            overall[name] = overall.get(name, 0) + value

    print("\nOverall result for both articles")
    header = f"{'Algorithm':<20}| Total time, s"
    print(header)
    print("-" * len(header))

    for name, value in sorted(overall.items(), key=lambda item: item[1]):
        print(f"{name:<20}| {value:.6f}")

    fastest = min(overall, key=overall.get)
    print(f"\nFastest algorithm overall: {fastest}")

    reference = 0.0
    for file_name, existing in zip(ARTICLES, existing_patterns):
        text = read_article(file_name)
        reference += measure(str.find, text, existing)
        reference += measure(str.find, text, fake_pattern)

    print(f"\nFor reference, the built-in str.find on the same data: {reference:.6f} s in total")


main()
