import numpy as np
import scipy.integrate as spi
import matplotlib.pyplot as plt
from pathlib import Path

A = 0.0
B = 2.0
ANALYTIC = 8 / 3
SAMPLE_SIZES = [10 ** power for power in range(2, 8)]
PLOT_FILE = "integral_plot.png"


def f(x):
    return x ** 2


# Mean value method: the integral equals the width of the interval multiplied by
# the average value of the function on it, and that average is estimated from a
# uniform random sample.
def monte_carlo_mean(a: float, b: float, samples: int, rng) -> float:
    points = rng.uniform(a, b, samples)
    return (b - a) * float(np.mean(f(points)))


# Hit or miss method: random points are thrown into the rectangle that bounds
# the curve, and the area under the curve is the area of the rectangle times the
# share of the points that landed below the graph. It requires f(x) >= 0 on the
# interval, which holds for x^2.
def monte_carlo_hit_or_miss(a: float, b: float, samples: int, rng) -> float:
    height = float(np.max(f(np.linspace(a, b, 1_000))))
    x = rng.uniform(a, b, samples)
    y = rng.uniform(0.0, height, samples)
    hits = int(np.count_nonzero(y <= f(x)))
    return (b - a) * height * hits / samples


def draw_plot(path: Path) -> None:
    x = np.linspace(-0.5, 2.5, 400)
    y = f(x)

    figure, (left, right) = plt.subplots(1, 2, figsize=(12, 5))

    left.plot(x, y, "r", linewidth=2)
    shaded = np.linspace(A, B)
    left.fill_between(shaded, f(shaded), color="gray", alpha=0.3)
    left.axvline(x=A, color="gray", linestyle="--")
    left.axvline(x=B, color="gray", linestyle="--")
    left.set_xlim([x[0], x[-1]])
    left.set_ylim([0, max(y) + 0.1])
    left.set_xlabel("x")
    left.set_ylabel("f(x)")
    left.set_title(f"Area under f(x) = x^2 from {A:g} to {B:g}")
    left.grid()

    rng = np.random.default_rng(1)
    height = float(f(B))
    sample_x = rng.uniform(A, B, 2_000)
    sample_y = rng.uniform(0.0, height, 2_000)
    inside = sample_y <= f(sample_x)

    right.plot(x, y, "r", linewidth=2)
    right.scatter(sample_x[inside], sample_y[inside], s=4, color="tab:green", alpha=0.5, label="under the curve")
    right.scatter(sample_x[~inside], sample_y[~inside], s=4, color="tab:red", alpha=0.5, label="above the curve")
    right.set_xlim([A, B])
    right.set_ylim([0, height])
    right.set_xlabel("x")
    right.set_ylabel("f(x)")
    right.set_title(f"Hit or miss method, 2000 points, {np.count_nonzero(inside)} hits")
    right.legend(loc="upper left")
    right.grid()

    figure.tight_layout()
    figure.savefig(path, dpi=120)
    print(f"Plot saved to {path.name}")
    plt.show()


def main() -> None:
    rng = np.random.default_rng(42)

    quad_result, quad_error = spi.quad(f, A, B)
    print(f"Integral of f(x) = x^2 from {A:g} to {B:g}")
    print(f"  analytic value  (b^3 - a^3) / 3 = {ANALYTIC:.10f}")
    print(f"  scipy quad                      = {quad_result:.10f}, estimated error {quad_error:.2e}")

    print("\nMonte Carlo, convergence with the number of samples")
    header = (f"{'Samples':<12}| {'Mean value':<14}| {'Error':<12}| "
              f"{'Hit or miss':<14}| {'Error':<12}| 1 / sqrt(N)")
    print(header)
    print("-" * len(header))

    for samples in SAMPLE_SIZES:
        mean_value = monte_carlo_mean(A, B, samples, rng)
        hit_or_miss = monte_carlo_hit_or_miss(A, B, samples, rng)
        print(f"{samples:<12}| {mean_value:<14.6f}| {abs(mean_value - quad_result):<12.6f}| "
              f"{hit_or_miss:<14.6f}| {abs(hit_or_miss - quad_result):<12.6f}| {1 / np.sqrt(samples):.6f}")

    runs = 50
    samples = 100_000
    print(f"\nStability of the estimate, {runs} independent runs of {samples} samples each")

    for title, method in (("Mean value", monte_carlo_mean), ("Hit or miss", monte_carlo_hit_or_miss)):
        estimates = np.array([method(A, B, samples, rng) for _ in range(runs)])

        print(f"  {title}")
        print(f"    average of the runs          = {estimates.mean():.6f}")
        print(f"    standard deviation           = {estimates.std(ddof=1):.6f}")
        print(f"    largest deviation from quad  = {np.abs(estimates - quad_result).max():.6f}")
        print(f"    relative error of the average = "
              f"{abs(estimates.mean() - quad_result) / quad_result * 100:.4f} %")

    draw_plot(Path(__file__).parent / PLOT_FILE)


main()
