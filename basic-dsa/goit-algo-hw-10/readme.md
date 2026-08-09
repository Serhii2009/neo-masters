# Homework 10

- `task_1.py` - change dispensing, greedy algorithm against dynamic programming
- `task_2.py` - definite integral by the Monte Carlo method, plot saved to `integral_plot.png`

```bash
pip install -r requirements.txt
python task_1.py
python task_2.py
```

Environment for all measurements: Python 3.11, Windows 11, Intel Core 12th generation.

---

## Task 1: change dispensing

Denominations `[50, 25, 10, 5, 2, 1]`.

`find_coins_greedy` walks the denominations from the largest down and takes as many coins of each as
fit. It touches every denomination once, so it is **O(k)** and does not depend on the amount.

`find_min_coins` fills a table of minimal coin counts for every sum up to the requested amount and a
second table with the last coin used, which lets the answer be restored backwards. That is
**O(n \* k)** in time and **O(n)** in memory.

For 113 the greedy one returns `{50: 2, 10: 1, 2: 1, 1: 1}` and the dynamic one
`{1: 1, 2: 1, 10: 1, 50: 2}`.

### Average time of one call, seconds

| Amount    | Greedy     | Dynamic    | Dynamic / Greedy |
| --------- | ---------- | ---------- | ---------------- |
| 113       | 0.00000061 | 0.00003878 | 64               |
| 1 000     | 0.00000028 | 0.00033597 | 1 180            |
| 10 000    | 0.00000026 | 0.00341103 | 13 175           |
| 100 000   | 0.00000031 | 0.03686920 | 119 434          |
| 1 000 000 | 0.00000028 | 0.39355170 | 1 416 673        |

### Conclusions

1. For large amounts the greedy algorithm is far more efficient. Its time stays at about
   0.3 microseconds across four orders of magnitude of the amount, while dynamic programming grows
   strictly linearly: every tenfold increase of the amount multiplies the time by about 10.7.

2. At an amount of 1 000 000 dynamic programming is 1.4 million times slower and allocates two lists
   of a million elements to return a dictionary with one entry. The gap keeps widening
   proportionally to the amount.

3. Speed is not the only criterion. The program checks both algorithms on every amount from 1 to
   5000: on `[50, 25, 10, 5, 2, 1]` the greedy result is minimal every time, but on `[25, 10, 1]` it
   fails for 30 amounts out of the first 100. For 30 it returns six coins, `{25: 1, 1: 5}`, instead
   of three, `{10: 3}`.

4. The coincidence on the first set is not luck. Kozen and Zaks proved that for a non-canonical coin
   system the smallest counterexample is always smaller than the sum of the two largest
   denominations, here 25 + 50 = 75. The check covers amounts far beyond that, so the greedy
   algorithm is provably optimal for this set for any amount.

5. For a cash register with a fixed set of denominations the greedy algorithm is the right choice.
   Dynamic programming is needed when the set changes and stops being canonical, and the sensible
   compromise is to run it once at configuration time as a check, then serve every transaction in
   O(k).

---

## Task 2: integral by the Monte Carlo method

Function `f(x) = x^2` on the interval from 0 to 2, analytic value `8 / 3 = 2.6666666667`.

Two variants are implemented: the **mean value method**, which multiplies the width of the interval
by the average value of the function on a uniform random sample, and the **hit or miss method**,
which throws points into the bounding rectangle and takes the share that landed under the curve.
The second one is the direct geometric reading of "find the area of the grey zone" and is what the
right panel of the plot shows.

`scipy.integrate.quad` returns 2.6666666667 with an estimated error of 2.96e-14.

### Convergence

| Samples    | Mean value | Error    | Hit or miss | Error    | 1 / sqrt(N) |
| ---------- | ---------- | -------- | ----------- | -------- | ----------- |
| 100        | 2.488111   | 0.178556 | 3.040000    | 0.373333 | 0.100000    |
| 1 000      | 2.676212   | 0.009545 | 2.672000    | 0.005333 | 0.031623    |
| 10 000     | 2.630292   | 0.036374 | 2.748000    | 0.081333 | 0.010000    |
| 100 000    | 2.668944   | 0.002277 | 2.676960    | 0.010293 | 0.003162    |
| 1 000 000  | 2.665442   | 0.001225 | 2.670792    | 0.004125 | 0.001000    |
| 10 000 000 | 2.667001   | 0.000334 | 2.667293    | 0.000626 | 0.000316    |

50 independent runs of 100 000 samples each:

| Method      | Average  | Standard deviation | Relative error of the average |
| ----------- | -------- | ------------------ | ----------------------------- |
| Mean value  | 2.666542 | 0.007174           | 0.0047 %                      |
| Hit or miss | 2.664784 | 0.012786           | 0.0706 %                      |

### Conclusions

1. The Monte Carlo result agrees with `quad` and with the analytic value. At ten million samples the
   relative error is 0.0125 percent, and the average of 50 runs differs from `quad` by 0.0047
   percent. The discrepancy is statistical noise, not a systematic bias, which confirms that both
   the implementation and the method are correct.

2. The error follows 1 / sqrt(N), and this can be checked numerically rather than by eye. The
   theoretical standard deviation of the mean value estimate at 100 000 samples is 0.007542, and the
   measurement over 50 runs gives 0.007174. Each extra decimal digit of accuracy costs a hundredfold
   increase in the number of points.

3. A single run proves nothing: in the table the row for 10 000 samples is worse than the row for
   1 000. The law describes the expected error, not one particular realisation, which is why the
   repeated experiment is needed.

4. The mean value method is the better of the two. With the same number of points its standard
   deviation is 1.78 times smaller, so hit or miss needs about 2.5 times more points for the same
   accuracy: it reduces every point to one bit and throws away the value of the function.

5. For a smooth function of one variable Monte Carlo is not the right tool. `quad` reaches machine
   precision instantly because Gauss-Kronrod quadrature integrates low-degree polynomials exactly,
   while Monte Carlo needs ten million evaluations for an error of 1e-4. The method earns its place
   in high-dimensional integrals, where a grid grows exponentially with the number of variables but
   the Monte Carlo error stays 1 / sqrt(N) regardless of dimension.
