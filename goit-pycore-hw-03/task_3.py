import re

def normalize_phone(phone_number: str) -> str:
    cleaned = re.sub(r"[^\d+]", "", phone_number)

    if cleaned.startswith("+"):
        pass
    elif cleaned.startswith("380"):
        cleaned = "+" + cleaned
    else:
        cleaned = "+38" + cleaned

    return cleaned

# Let's Test!
raw_numbers = [
        "067\t123 4567",
        "(095) 234-5678\n",
        "+380 44 123 4567",
        "380501234567",
        "    +38(050)123-32-34",
        "     0503451234",
        "(050)8889900",
        "38050-111-22-22",
        "38050 111 22 11   ",
    ]

sanitized_numbers = [normalize_phone(number) for number in raw_numbers]
print("Normalized phone numbers:", sanitized_numbers)