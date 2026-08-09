items = {
    "pizza": {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog": {"cost": 30, "calories": 200},
    "pepsi": {"cost": 10, "calories": 100},
    "cola": {"cost": 15, "calories": 220},
    "potato": {"cost": 25, "calories": 350},
}

BUDGETS = [40, 60, 80, 100, 120]


def greedy_algorithm(items: dict, budget: int) -> tuple:
    ordered = sorted(
        items.items(),
        key=lambda entry: entry[1]["calories"] / entry[1]["cost"],
        reverse=True,
    )

    chosen = []
    spent = 0
    calories = 0

    for name, item in ordered:
        if spent + item["cost"] <= budget:
            chosen.append(name)
            spent += item["cost"]
            calories += item["calories"]

    return chosen, spent, calories


def dynamic_programming(items: dict, budget: int) -> tuple:
    names = list(items)
    table = [[0] * (budget + 1) for _ in range(len(names) + 1)]

    for index in range(1, len(names) + 1):
        cost = items[names[index - 1]]["cost"]
        calories = items[names[index - 1]]["calories"]

        for money in range(budget + 1):
            table[index][money] = table[index - 1][money]

            if cost <= money:
                with_item = table[index - 1][money - cost] + calories
                table[index][money] = max(table[index][money], with_item)

    chosen = []
    money = budget

    for index in range(len(names), 0, -1):
        if table[index][money] != table[index - 1][money]:
            name = names[index - 1]
            chosen.append(name)
            money -= items[name]["cost"]

    chosen.reverse()
    spent = sum(items[name]["cost"] for name in chosen)
    return chosen, spent, table[len(names)][budget]


def main() -> None:
    print("Menu")
    header = f"{'Dish':<12}| {'Cost':<6}| {'Calories':<10}| Calories per unit of cost"
    print(header)
    print("-" * len(header))

    for name, item in items.items():
        ratio = item["calories"] / item["cost"]
        print(f"{name:<12}| {item['cost']:<6}| {item['calories']:<10}| {ratio:.2f}")

    print("\nComparison of the two approaches")
    header = (f"{'Budget':<8}| {'Greedy calories':<17}| {'Dynamic calories':<18}| "
              f"{'Loss':<6}| Greedy set")
    print(header)
    print("-" * (len(header) + 30))

    for budget in BUDGETS:
        greedy_set, greedy_spent, greedy_calories = greedy_algorithm(items, budget)
        dynamic_set, dynamic_spent, dynamic_calories = dynamic_programming(items, budget)
        loss = dynamic_calories - greedy_calories

        print(f"{budget:<8}| {greedy_calories:<17}| {dynamic_calories:<18}| "
              f"{loss:<6}| {', '.join(greedy_set)}")

    print("\nDetailed result for a budget of 100")
    for title, solver in (("Greedy", greedy_algorithm), ("Dynamic", dynamic_programming)):
        chosen, spent, calories = solver(items, 100)
        print(f"  {title}")
        print(f"    dishes:   {', '.join(chosen)}")
        print(f"    cost:     {spent}")
        print(f"    calories: {calories}")


main()
