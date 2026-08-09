# Homework 4

- `task_1.py` - recursively copies files and sorts them into subdirectories by extension
- `task_2.py` - draws the Koch snowflake with a user-defined recursion level
- `task_3.py` - compares sorting algorithms

```bash
python task_1.py <source> [destination]   # destination defaults to dist
python task_2.py [level]                  # asks for the level if not passed
python task_3.py
```

## Task 3: comparison of sorting algorithms

Four algorithms on four data distributions: insertion sort, merge sort, a hybrid (merge sort that
switches to insertion sort on runs of 32 elements or fewer) and the built-in Timsort. Time is
measured with `timeit`, every run gets a fresh copy of the array, the data is generated with a fixed
seed.

Environment: Python 3.11, Windows 11, Intel Core 12th generation.

### Average time per run, seconds

| Data          | Size  | Insertion | Merge   | Hybrid  | Timsort |
| ------------- | ----- | --------- | ------- | ------- | ------- |
| random        | 1000  | 0.01072   | 0.00108 | 0.00083 | 0.00007 |
| random        | 5000  | 0.29016   | 0.00658 | 0.00497 | 0.00047 |
| random        | 10000 | 1.19545   | 0.01290 | 0.00978 | 0.00099 |
| sorted        | 1000  | 0.00006   | 0.00067 | 0.00025 | 0.00001 |
| sorted        | 5000  | 0.00028   | 0.00384 | 0.00199 | 0.00003 |
| sorted        | 10000 | 0.00057   | 0.00859 | 0.00493 | 0.00011 |
| reversed      | 1000  | 0.02130   | 0.00086 | 0.00093 | 0.00001 |
| reversed      | 5000  | 0.57573   | 0.00432 | 0.00417 | 0.00004 |
| reversed      | 10000 | 2.33004   | 0.01202 | 0.00956 | 0.00013 |
| nearly sorted | 1000  | 0.00176   | 0.00084 | 0.00048 | 0.00002 |
| nearly sorted | 5000  | 0.03921   | 0.00519 | 0.00320 | 0.00015 |
| nearly sorted | 10000 | 0.14209   | 0.01264 | 0.00823 | 0.00038 |

Large arrays, without insertion sort:

| Data          | Size   | Merge   | Hybrid  | Timsort |
| ------------- | ------ | ------- | ------- | ------- |
| random        | 50000  | 0.08314 | 0.06669 | 0.00643 |
| random        | 100000 | 0.17066 | 0.14220 | 0.01564 |
| random        | 500000 | 1.09044 | 0.96199 | 0.09920 |
| sorted        | 500000 | 0.60050 | 0.37829 | 0.00833 |
| reversed      | 500000 | 0.60794 | 0.68602 | 0.01012 |
| nearly sorted | 500000 | 0.90214 | 0.67939 | 0.03392 |

### Conclusions

1. Insertion sort behaves exactly as O(n^2) predicts. Growing the array five times increases the
   time 27.1 times (theory 25), doubling it increases the time 4.12 times (theory 4). On sorted data
   it degenerates to O(n) and becomes the fastest of the own implementations, on reversed data it
   hits its worst case and is 1.95 times slower than on random data.

2. Merge sort is O(n log n) for any input order. Doubling the size from 50000 to 100000 gives a
   factor of 2.05 against the theoretical 2.13. Across the four distributions its time varies only
   1.5 times, while insertion sort varies more than 4000 times, and that predictability is its main
   advantage.

3. At 10000 elements insertion sort is already 93 times slower than merge sort on random data and
   194 times slower on reversed data. Beyond 100000 elements it is unusable.

4. Adding insertion sort to merge sort gives a speedup of 1.2 to 1.7 times, and the gain is largest
   on ordered data where insertion sort is at its best. This is exactly the idea Timsort is built
   on. The hybrid loses only on the reversed array, where every short run is the worst case for
   insertion sort; real Timsort avoids this by detecting descending runs and reversing them.

5. Timsort is 13 times faster than merge sort on random data and 72 times faster on sorted data.
   Part of that gap comes from the C implementation, but the algorithmic part is visible in the
   hybrid, which is written in the same language and still wins up to 1.7 times.

6. In practice there is no reason to write a sorting algorithm by hand. `sorted()` and `list.sort()`
   are faster by one or two orders of magnitude, are stable, work with any comparable type and
   accept a `key` argument.
