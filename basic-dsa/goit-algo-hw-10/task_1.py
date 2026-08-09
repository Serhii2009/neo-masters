import timeit

COINS = [50, 25, 10, 5, 2, 1]
AMOUNTS = [113, 1_000, 10_000, 100_000, 1_000_000]


# The greedy algorithm takes as many coins of the largest denomination as
# possible and moves on to the next one. It touches every denomination exactly
# once, so its complexity is O(k) for k denominations and does not depend on the
# amount at all.
def find_coins_greedy(amount: int, coins: list = COINS) -> dict:
    result = {}

    for coin in sorted(coins, reverse=True):
        if amount <= 0:
            break

        count, amount = divmod(amount, coin)

        if count:
            result[coin] = count

    return result


# Dynamic programming builds the answer for every sum from 1 to the requested
# amount, so its complexity is O(n * k) in time and O(n) in memory. In exchange
# it gives the provably minimal number of coins for any set of denominations.
def find_min_coins(amount: int, coins: list = COINS) -> dict:
    if amount <= 0:
        return {}

    unreachable = amount + 1
    min_coins = [0] + [unreachable] * amount
    last_coin = [0] * (amount + 1)

    for value in range(1, amount + 1):
        for coin in coins:
            if coin <= value and min_coins[value - coin] + 1 < min_coins[value]:
                min_coins[value] = min_coins[value - coin] + 1
                last_coin[value] = coin

    if min_coins[amount] == unreachable:
        return {}

    result = {}
    remainder = amount

    while remainder > 0:
        coin = last_coin[remainder]
        result[coin] = result.get(coin, 0) + 1
        remainder -= coin

    return dict(sorted(result.items()))


def total_coins(change: dict) -> int:
    return sum(change.values())


def compare_on_set(coins: list, limit: int) -> list:
    return [
        amount
        for amount in range(1, limit + 1)
        if total_coins(find_coins_greedy(amount, coins)) != total_coins(find_min_coins(amount, coins))
    ]


def measure(function, amount: int, repeats: int) -> float:
    timer = timeit.Timer(lambda: function(amount))
    return timer.timeit(number=repeats) / repeats


def main() -> None:
    print(f"Denominations: {COINS}\n")

    for amount in (113, 1_000):
        print(f"Change for {amount}")
        print(f"  greedy:  {find_coins_greedy(amount)}")
        print(f"  dynamic: {find_min_coins(amount)}")
        print()

    limit = 5_000
    mismatches = compare_on_set(COINS, limit)
    print(f"Amounts from 1 to {limit} where the greedy result is not minimal: {len(mismatches)}")

    broken_set = [25, 10, 1]
    broken_mismatches = compare_on_set(broken_set, 100)
    example = broken_mismatches[0]
    print(f"\nThe same check on the set {broken_set}: {len(broken_mismatches)} amounts out of 100")
    print(f"  for example, {example}")
    print(f"    greedy:  {find_coins_greedy(example, broken_set)}"
          f" -> {total_coins(find_coins_greedy(example, broken_set))} coins")
    print(f"    dynamic: {find_min_coins(example, broken_set)}"
          f" -> {total_coins(find_min_coins(example, broken_set))} coins")

    print("\nExecution time, average of one call in seconds")
    header = f"{'Amount':<12}| {'Greedy':<14}| {'Dynamic':<14}| Dynamic / Greedy"
    print(header)
    print("-" * len(header))

    for amount in AMOUNTS:
        greedy_time = measure(find_coins_greedy, amount, 1_000)
        dynamic_time = measure(find_min_coins, amount, 20 if amount <= 10_000 else 1)
        print(f"{amount:<12}| {greedy_time:<14.8f}| {dynamic_time:<14.8f}| {dynamic_time / greedy_time:.0f}")


main()
