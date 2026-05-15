import random

def get_numbers_ticket(min: int, max: int, quantity: int) -> list[int]:
    if min < 1 or max > 1000 or quantity < 1 or quantity > (max - min + 1):
        return []
    
    return sorted(random.sample(range(min, max + 1), quantity))

# Let's Test!
lottery_numbers = get_numbers_ticket(1, 45, 7)
print("Your lottery numbers:", lottery_numbers)