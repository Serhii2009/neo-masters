# Homework 5

Comparison of three substring search algorithms on two articles.

```bash
python task_1.py
```

## Implementation

- **Boyer-Moore** with the bad character heuristic, compares the pattern from right to left and
  shifts it by the distance from a precomputed table
- **Knuth-Morris-Pratt** with the prefix function, never moves the text pointer backwards
- **Rabin-Karp** with a rolling polynomial hash, compares substrings only when the hashes match

All three return the index of the first occurrence or -1. Before benchmarking they were checked
against the built-in `str.find` on about 9000 generated cases, including Cyrillic text, empty
patterns and patterns longer than the text.

## Search patterns

| Article       | Length | Existing pattern          | Position   | Non-existing pattern       |
| ------------- | ------ | ------------------------- | ---------- | -------------------------- |
| article_1.txt | 12527  | `оптимізаційних задач`    | 8415 (67%) | `квантовий блокчейн даних` |
| article_2.txt | 18422  | `бінарних діаграм рішень` | 14605 (79%)| `квантовий блокчейн даних` |

Both existing patterns occur once and sit in the last third of the text, so the algorithms have to
scan almost the whole article. All patterns are 20 to 24 characters long, so their length does not
distort the comparison.

## Results

Average time of one search in seconds, 50 runs per measurement. Python 3.11, Windows 11, Intel Core
12th generation.

| Article       | Algorithm          | Existing | Non-existing | Total    |
| ------------- | ------------------ | -------- | ------------ | -------- |
| article_1.txt | Boyer-Moore        | 0.000147 | 0.000178     | 0.000326 |
| article_1.txt | Knuth-Morris-Pratt | 0.000755 | 0.000972     | 0.001727 |
| article_1.txt | Rabin-Karp         | 0.001743 | 0.002638     | 0.004381 |
| article_2.txt | Boyer-Moore        | 0.000254 | 0.000313     | 0.000567 |
| article_2.txt | Knuth-Morris-Pratt | 0.001226 | 0.001625     | 0.002851 |
| article_2.txt | Rabin-Karp         | 0.003055 | 0.003735     | 0.006790 |

Both articles together: Boyer-Moore 0.000893 s, Knuth-Morris-Pratt 0.004578 s (5.13 times slower),
Rabin-Karp 0.011170 s (12.51 times slower). The built-in `str.find` needs 0.000005 s for the same
four searches.

## Conclusions

1. **For article 1 the fastest algorithm is Boyer-Moore**: 0.000326 s against 0.001727 s for
   Knuth-Morris-Pratt and 0.004381 s for Rabin-Karp.

2. **For article 2 the fastest algorithm is also Boyer-Moore**: 0.000567 s against 0.002851 s and
   0.006790 s.

3. **Overall Boyer-Moore wins as well**, being 5.13 times faster than Knuth-Morris-Pratt and 12.51
   times faster than Rabin-Karp. It leads in all four measurements, so the result does not depend on
   the text or on whether the pattern exists.

4. The reason is the data rather than a general superiority of the algorithm. The patterns are long
   and the Ukrainian alphabet is large, so most characters of the text do not occur in the pattern
   at all and every mismatch shifts the pattern by its full length. On a small alphabet, for example
   a DNA sequence, or on a short pattern the shifts would shrink and Knuth-Morris-Pratt would catch
   up.

5. Knuth-Morris-Pratt is stable but has nothing to skip: it reads every character exactly once. Its
   guaranteed O(n + m) matters on data where the Boyer-Moore shift table degenerates, which does not
   happen in natural language.

6. Rabin-Karp is the worst choice here. It does far more work per position, and the small modulus
   101 gives about one false hash match per hundred windows, roughly 180 extra comparisons per search
   on article 2. It pays off only when many patterns are searched at once.

7. Searching a non-existing pattern is always slower, by 21 to 51 percent depending on the
   algorithm, because the whole text has to be scanned. The ranking stays the same.

8. As with the sorting homework, the built-in implementation wins by a wide margin: `str.find` is
   about 180 times faster than the best of the three, because it is written in C and combines a
   Horspool-style skip with a Bloom filter of the pattern characters.
