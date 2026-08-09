import random
from pathlib import Path
from collections import Counter

import matplotlib.pyplot as plt

SUMS = list(range(2, 13))
SAMPLE_SIZES = [1_000, 10_000, 100_000, 1_000_000]
PLOT_FILE = "dice_probabilities.png"

COMBINATIONS = {2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 5, 9: 4, 10: 3, 11: 2, 12: 1}
ANALYTICAL = {total: ways / 36 for total, ways in COMBINATIONS.items()}


def simulate(rolls: int, generator: random.Random) -> Counter:
    counts = Counter()

    for _ in range(rolls):
        counts[generator.randint(1, 6) + generator.randint(1, 6)] += 1

    return counts


def probabilities(counts: Counter, rolls: int) -> dict:
    return {total: counts[total] / rolls for total in SUMS}


def print_table(estimated: dict, rolls: int) -> None:
    print(f"Monte Carlo with {rolls:,} rolls".replace(",", " "))
    header = f"{'Sum':<5}| {'Simulated':<12}| {'Analytical':<12}| {'Ways':<6}| Difference"
    print(header)
    print("-" * len(header))

    for total in SUMS:
        exact = ANALYTICAL[total]
        value = estimated[total]
        print(f"{total:<5}| {value * 100:>10.2f} % | {exact * 100:>10.2f} % | "
              f"{COMBINATIONS[total]:>2}/36 | {abs(value - exact) * 100:>6.3f} pp")

    print()


def draw_plot(estimated: dict, rolls: int, path: Path) -> None:
    figure, axes = plt.subplots(figsize=(10, 6))

    axes.bar(SUMS, [estimated[total] * 100 for total in SUMS],
             color="#5B9BD5", label=f"Monte Carlo, {rolls:,} rolls".replace(",", " "))
    axes.plot(SUMS, [ANALYTICAL[total] * 100 for total in SUMS],
              color="#C00000", marker="o", linewidth=2, label="Analytical, ways out of 36")

    for total in SUMS:
        axes.annotate(f"{estimated[total] * 100:.2f}",
                      (total, estimated[total] * 100),
                      textcoords="offset points", xytext=(0, 13),
                      ha="center", fontsize=8)

    axes.set_xticks(SUMS)
    axes.set_xlabel("Sum of two dice")
    axes.set_ylabel("Probability, %")
    axes.set_title("Probability of each sum when throwing two dice")
    axes.grid(axis="y", alpha=0.3)
    axes.legend()

    figure.tight_layout()
    figure.savefig(path, dpi=120)
    print(f"Plot saved to {path.name}")
    plt.show()


def main() -> None:
    generator = random.Random(42)

    print("Convergence of the simulation")
    header = f"{'Rolls':<12}| {'Largest error':<16}| Mean error"
    print(header)
    print("-" * len(header))

    largest = None

    for rolls in SAMPLE_SIZES:
        estimated = probabilities(simulate(rolls, generator), rolls)
        errors = [abs(estimated[total] - ANALYTICAL[total]) for total in SUMS]

        print(f"{rolls:<12}| {max(errors) * 100:>13.3f} pp | {sum(errors) / len(errors) * 100:>9.3f} pp")
        largest = (estimated, rolls)

    print()
    print_table(*largest)
    draw_plot(*largest, Path(__file__).parent / PLOT_FILE)


main()
