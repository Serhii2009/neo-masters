from collections import deque


def normalize(text: str) -> deque:
    return deque(char.lower() for char in text if char.isalnum())


def is_palindrome(text: str) -> bool:
    characters = normalize(text)

    while len(characters) > 1:
        if characters.popleft() != characters.pop():
            return False

    return True


def main() -> None:
    samples = [
        "Level",
        "Abba",
        "A man a plan a canal Panama",
        "Never odd or even",
        "Python",
        "Hello world",
        "",
    ]

    print(f"{'String':<30}| {'Length':<7}| Result")
    print(f"{'-' * 30}|{'-' * 8}|--------------------")

    for text in samples:
        length = len(normalize(text))
        result = "palindrome" if is_palindrome(text) else "not a palindrome"
        print(f"{text or '(empty)':<30}| {length:<7}| {result}")


main()
