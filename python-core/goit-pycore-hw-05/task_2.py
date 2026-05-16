import re
from typing import Callable


def generator_numbers(text: str):
    for match in re.finditer(r"(?<= )\d+\.\d+(?= )", text):
        yield float(match.group())


def sum_profit(text: str, func: Callable) -> float:
    return sum(func(text))

# Let's Test!
text = (
    "The employee's total income consists of several parts: "
    "1000.01 as the main income, supplemented by additional "
    "earnings of 27.45 and 324.00 dollars."
)
total_income = sum_profit(text, generator_numbers)
print(f"Total income: {total_income}")