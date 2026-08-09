# Final project

Seven independent tasks covering the topics of the course.

| File              | Task                                                              |
| ----------------- | ----------------------------------------------------------------- |
| `task_1.py`       | 1. Singly linked list: reversal, merge sort, merging sorted lists  |
| `task_2.py`       | 2. Pythagoras tree fractal with a user-defined recursion level     |
| `task_3.py`       | 3. Dijkstra shortest paths on a binary heap                        |
| `task_4.py`       | 4. Visualisation of a binary heap                                  |
| `task_5.py`       | 5. Visualisation of depth first and breadth first traversal        |
| `task_6.py`       | 6. Greedy algorithm and dynamic programming for a limited budget   |
| `task_7.py`       | 7. Monte Carlo simulation of throwing two dice                     |
| `binary_tree.py`  | Shared tree drawing code used by tasks 4 and 5                     |

## How to run

```bash
pip install -r requirements.txt

python task_1.py
python task_2.py 8        # the level can also be entered interactively
python task_3.py
python task_4.py
python task_5.py
python task_6.py
python task_7.py
```

Tasks 4, 5 and 7 also save their figures next to the scripts: `heap_tree.png`,
`dfs_traversal.png`, `bfs_traversal.png` and `dice_probabilities.png`.

Environment: Python 3.11, Windows 11, Intel Core 12th generation.

## Notes on the implementation

**Task 1.** Merge sort was chosen over insertion sort because a linked list has no random
access: merge sort splits the list with the slow and fast pointer technique, needs only pointer
rewiring and runs in O(n log n) instead of O(n^2). Reversal changes the `next` pointers in place
and creates no new nodes.

**Task 3.** The binary heap always returns the unvisited vertex with the smallest known distance
in O(log n), which turns the O(V^2) scan of the naive version into O((V + E) log V). A vertex can
be pushed into the heap several times; the first pop holds the final distance and every later copy
is skipped through the visited set. The distances produced by the implementation were compared
with `networkx.single_source_dijkstra_path_length` for all seven start vertices, and every
reconstructed path was checked to have exactly the claimed total weight.

**Task 4.** The tree is built directly from the heap array: the children of the element with
index `i` are located at `2i + 1` and `2i + 2`, so no separate tree structure is needed.

**Task 5.** Both traversals use an explicit data structure rather than recursion: depth first
search on a stack, with the right child pushed first so that the left subtree is visited first,
and breadth first search on a queue. Colours are interpolated in RGB from `#0A2A5C` to `#B0E2FF`,
so the first visited node is the darkest and the last one the lightest. The label colour follows
the brightness of the node, otherwise black text on a dark node would be unreadable.

**Task 6.** The greedy algorithm sorts the dishes by calories per unit of cost and takes them
while the budget allows, which is O(n log n). Dynamic programming solves the zero-one knapsack
problem, where cost plays the role of weight and calories the role of value, in O(n * budget).

## Task 6: greedy algorithm against dynamic programming

| Budget | Greedy calories | Dynamic calories | Loss |
| ------ | --------------- | ---------------- | ---- |
| 40     | 570             | 570              | 0    |
| 60     | 670             | 670              | 0    |
| 80     | 870             | 870              | 0    |
| 100    | 870             | 970              | 100  |
| 120    | 1120            | 1120             | 0    |

For a budget of 100 the greedy algorithm returns cola, potato, pepsi and hot-dog: 870 calories for
80 units of money. It ranks hot-dog above pizza because the ratio of hot-dog is higher, and after
taking it there is no room left for anything else. Dynamic programming gives up that local gain and
returns pizza, pepsi, cola and potato: 970 calories for exactly 100 units. The greedy answer is
optimal for four budgets out of five, but it offers no guarantee, and the case of 100 shows the
price of that.

## Task 7: Monte Carlo simulation of two dice

Two dice are thrown a large number of times, the sum of each throw is counted, and the frequency of
each sum is divided by the number of throws. The result is compared with the exact probabilities,
which follow from the fact that 36 outcomes are equally likely and a given sum can be obtained in a
fixed number of ways.

### Result of 1 000 000 throws

| Sum | Simulated | Analytical | Ways  | Difference |
| --- | --------- | ---------- | ----- | ---------- |
| 2   | 2.81 %    | 2.78 %     | 1/36  | 0.029 pp   |
| 3   | 5.52 %    | 5.56 %     | 2/36  | 0.034 pp   |
| 4   | 8.33 %    | 8.33 %     | 3/36  | 0.001 pp   |
| 5   | 11.09 %   | 11.11 %    | 4/36  | 0.019 pp   |
| 6   | 13.89 %   | 13.89 %    | 5/36  | 0.002 pp   |
| 7   | 16.66 %   | 16.67 %    | 6/36  | 0.002 pp   |
| 8   | 13.92 %   | 13.89 %    | 5/36  | 0.034 pp   |
| 9   | 11.14 %   | 11.11 %    | 4/36  | 0.025 pp   |
| 10  | 8.29 %    | 8.33 %     | 3/36  | 0.042 pp   |
| 11  | 5.58 %    | 5.56 %     | 2/36  | 0.022 pp   |
| 12  | 2.76 %    | 2.78 %     | 1/36  | 0.015 pp   |

### Convergence

| Throws    | Largest error | Mean error | Mean error predicted by theory |
| --------- | ------------- | ---------- | ------------------------------ |
| 1 000     | 1.489 pp      | 0.743 pp   | 0.696 pp                       |
| 10 000    | 0.263 pp      | 0.121 pp   | 0.220 pp                       |
| 100 000   | 0.219 pp      | 0.061 pp   | 0.070 pp                       |
| 1 000 000 | 0.042 pp      | 0.021 pp   | 0.022 pp                       |

The predicted column is not fitted to the measurement. The number of times a given sum appears is a
binomial variable, so the standard deviation of its estimated probability is the square root of
`p (1 - p) / N`, and the expected absolute deviation is that value multiplied by the square root of
`2 / pi`. The column is the average of this quantity over all eleven sums.

## Conclusions

1. **The Monte Carlo method reproduces the analytical probabilities.** After a million throws the
   largest deviation over all eleven sums is 0.042 percentage points and the mean deviation is
   0.021, that is, the simulated values agree with the exact ones to the second decimal place. The
   symmetry of the distribution is reproduced as well: 6 and 8 both give 13.89 and 13.92 percent
   against the exact 13.89, and 2 and 12 give 2.81 and 2.76 against 2.78.

2. **The accuracy is governed by the law of one over the square root of N, and this can be verified
   numerically rather than by eye.** At a million throws the theory predicts a mean deviation of
   0.022 percentage points and the measurement gives 0.021; at a hundred thousand the prediction is
   0.070 against a measured 0.061. Increasing the number of throws a hundredfold reduces the error
   roughly tenfold, so every extra decimal digit of accuracy costs a hundred times more computation.

3. **A single run proves nothing.** In the convergence table ten thousand throws happened to give a
   mean error of 0.121 while the theory expects 0.220, that is, the run was luckier than average.
   The law describes the expected error, not the error of one particular realisation, which is why
   the comparison is made across several sample sizes rather than on one.

4. **For this problem the analytical answer is better in every respect.** There are only 36
   outcomes, they can be enumerated by hand, and the result is exact. The simulation needed a
   million throws to reach two correct decimal places. The value of the Monte Carlo method appears
   where the space of outcomes cannot be enumerated: many dice, complicated rules, dependencies
   between events, or a distribution that has no closed form at all. The dice serve as a case where
   the exact answer is known, which is exactly what makes them useful for checking that the method
   and its implementation are correct.
