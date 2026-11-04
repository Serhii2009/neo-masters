# goit-rdb-hw-05

Homework 5 for the Relational Databases course (GoIT Neoversity): customer-level ML features in PostgreSQL. The notebook computes them with a CTE pipeline of named stages, walks a referral tree with a recursive CTE, caches the features in a materialized view with concurrent refresh, and compares recomputation with reading from the view using `EXPLAIN (ANALYZE, BUFFERS)`.

**Dataset:** Brazilian E-Commerce Public Dataset by Olist, about 100,000 orders from 2016 to 2018.
**Stack:** PostgreSQL 16 (via `pgserver`) in Google Colab, SQL cells via `jupysql`.

## Data source

| What | Link |
|---|---|
| Dataset page | [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) (Kaggle, `olistbr/brazilian-ecommerce`, version 2) |
| Files used | 5 of 9: customers, orders, order items, products, sellers |

## How the data gets into the database

1. `kagglehub.dataset_download("olistbr/brazilian-ecommerce")` downloads the public dataset without Kaggle credentials and caches it.
2. If the CSV files are placed in `data/olist/` next to the notebook (for example from the course archive), the notebook uses that copy and downloads nothing. The CSV files are not committed to this repository; Kaggle is the source.
3. `pandas.to_sql` loads each CSV into a raw table (`olist_*_raw`), and `INSERT INTO ... SELECT` with explicit casts moves the rows into the typed tables.

The real Olist data is used, so the stub schema from the assignment is not needed. It also makes the `EXPLAIN` plans meaningful, which they would not be on 100 rows.

| Typed table | Rows |
|---|---|
| `olist_customers` | 99,441 |
| `olist_orders` | 99,441 |
| `olist_order_items` | 112,650 |
| `olist_products` | 32,951 |
| `olist_sellers` | 3,095 |

No row is lost between the raw and the typed layer. The notebook also builds `hw5_referrals` (9 synthetic referrals) and the materialized view `mv_olist_customer_features` (99,441 rows, one per `customer_id`).

## Repository contents

| File | Description |
|---|---|
| `hw5_olist_features.ipynb` | Main notebook with all five tasks, executed end-to-end with outputs |
| `README.md` | This file |

## Where to find each task in the notebook

| Task | Section | What is there |
|---|---|---|
| 1. Setup and typed schema | 1 | `pgserver` and PostgreSQL version, download via `kagglehub`, raw tables, typed DDL, `INSERT ... SELECT`, row-count smoke test |
| 2. CTE pipeline | 2 | Eight named stages with `-- Stage N:` comments: reference date, order totals, RFM, cohort quarter, rolling 30-day AOV, cancellation rate, category revenue, preferred category; a grain check of `customer_id` vs. `customer_unique_id` |
| 3. Recursive CTE | 3 | `hw5_referrals`, depth and path with anchor, recursive part, `path_ids` and depth guards; the referral tree from real roots; a cycle A → B → A tested with both guards, with the depth guard only and with the `CYCLE` clause |
| 4. Materialized view | 4 | The full pipeline as `mv_olist_customer_features`, unique index, checks of every stage, `REFRESH ... CONCURRENTLY`, why a non-unique index fails, a freshness demo, refresh timings |
| 5. `EXPLAIN` and reflection | 5 | `EXPLAIN (ANALYZE, BUFFERS)` of the RFM stages, a view lookup, top-N from the view with and without an index, the full pipeline, the cost of each feature on its own, a summary table, reflection |

Section 6 runs assertions on the main results and prints `All checks passed`.

## Changes to the assignment templates

- **Index for the top-N query.** The suggested `CREATE INDEX ... (monetary DESC)` is created and explained as given, but PostgreSQL does not use it. `DESC` implies `NULLS FIRST`, while the query sorts `NULLS LAST`. The notebook shows this in the plan and then replaces it with `(monetary DESC NULLS LAST)`, which turns the plan into an `Index Scan`.
- The two checks of the view run in separate cells, because `jupysql` shows only the result of the last statement in a cell.
- `ANALYZE` runs right after the load, so the plans do not depend on when autovacuum collects statistics.
- `EXPLAIN` statements run through a small Python helper that prints the plan with its indentation; in a table cell the plan tree would be unreadable.
- The `pgserver` data directory is `hw5_pg` in the system temp folder, which is `/tmp/hw5_pg` on Colab, as in the template.

The typed DDL, the pipeline, the referral table, the recursive CTE and the materialized view are used exactly as given.

## How to run

1. Open `hw5_olist_features.ipynb` in Google Colab.
2. Select **Runtime → Restart session and run all**.

The first cell installs everything that is needed, and the data is downloaded from Kaggle without credentials, so there is nothing to upload or configure. Every section drops and recreates its objects, so repeated runs give the same results; only the `EXPLAIN` timings and the `referred_at` timestamps change. The notebook works on the current default Colab runtime (Python 3.13) as well as on Python 3.12, and also runs locally. The Windows build of `pgserver` has no time zone database, so there the session uses the equivalent POSIX rule `UTC0` instead of `UTC`; see section 1.1.
