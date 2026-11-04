# goit-rdb-hw-04

Homework 4 for the Relational Databases course (GoIT Neoversity): a multi-table e-commerce schema in PostgreSQL, from raw CSV files to typed tables with keys and constraints, then DML with PostgreSQL features, customer segmentation, JOINs, aggregates, set operations and a window function.

**Dataset:** Brazilian E-Commerce Public Dataset by Olist, about 100,000 orders from 2016 to 2018.
**Stack:** PostgreSQL 16 (via `pgserver`) in Google Colab, SQL cells via `jupysql`.

## Data source

| What | Link |
|---|---|
| Dataset page | [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) (Kaggle, `olistbr/brazilian-ecommerce`, version 2) |
| Files used | 6 of 9: customers, orders, order items, products, sellers, order reviews |

## How the data gets into the database

1. `kagglehub.dataset_download("olistbr/brazilian-ecommerce")` downloads the public dataset without Kaggle credentials and caches it.
2. If the CSV files are placed in `data/olist/` next to the notebook (for example from the course archive), the notebook uses that copy and downloads nothing. The CSV files are not committed to this repository; Kaggle is the source.
3. `pandas.to_sql` loads each CSV into a raw table (`olist_*_raw`), and `INSERT INTO ... SELECT` with explicit casts moves the rows into the typed tables.

| Typed table | Rows | Raw table rows |
|---|---|---|
| `olist_customers` | 99,441 | 99,441 |
| `olist_orders` | 99,441 | 99,441 |
| `olist_order_items` | 112,650 | 112,650 |
| `olist_products` | 32,951 | 32,951 |
| `olist_sellers` | 3,095 | 3,095 |
| `olist_order_reviews` | 99,224 | 99,224 |

No row is lost between the raw and the typed layer. The notebook also builds `seller_alerts`, `seller_score` (3,095 sellers), `olist_customer_dim` and `customer_segments` (96,096 real buyers each).

## Repository contents

| File | Description |
|---|---|
| `hw4_olist.ipynb` | Main notebook with all six tasks, executed end-to-end with outputs |
| `README.md` | This file |

## Where to find each task in the notebook

| Task | Section | What is there |
|---|---|---|
| 1. Setup and typed schema | 1 | `pgserver` and PostgreSQL version, download via `kagglehub`, raw tables, typed DDL, `INSERT ... SELECT`, row-count smoke test, data-quality profile |
| 2. DML | 2 | `INSERT ... RETURNING` alert; `ON CONFLICT DO UPDATE` upsert of `seller_score` with a second-run check and a comparison against the naive item-level join; `UPDATE ... FROM` for `is_late`, plus a version that only touches changed rows; `DELETE ... RETURNING` with a backdated alert to show that the filter works |
| 3. `customer_segments` | 3 | Customer dimension per `customer_unique_id`, DDL with identity PK, `UNIQUE`, FK, `CHECK`, `NOT NULL` and `DEFAULT`, idempotent fill with a data-derived reference date, constraint check, segment summary |
| 4. JOIN queries | 4 | `INNER JOIN` on four tables, `LEFT JOIN` + `COALESCE`, `FULL OUTER JOIN`, `SELF JOIN`, anti-join as `LEFT JOIN ... IS NULL` and `NOT EXISTS` |
| 5. Aggregates | 5 | Three aggregate queries with `HAVING`, `STRING_AGG`, `WHERE` vs. `HAVING` |
| 6. Set operations, window, reflection | 6 | `UNION`, `INTERSECT`, `EXCEPT`, `ROW_NUMBER()` and `COUNT(*) OVER`, reflection |

Section 7 runs assertions on the main results and prints `All checks passed`.

## Changes to the assignment templates

- **5.3** uses `HAVING COUNT(DISTINCT o.order_id) >= 2` instead of `>= 1`. After the `INNER JOIN` with orders every buyer has at least one order, so `>= 1` filters nothing; `>= 2` turns the query into a list of repeat buyers.
- Queries that end with `LIMIT` got an extra `ORDER BY` key where rows could tie, so their output is deterministic.
- The `pgserver` data directory is `hw4_pg` in the system temp folder, which is `/tmp/hw4_pg` on Colab, as in the template.

The typed DDL and the DML and segmentation statements are used exactly as given. Some cells add a `SELECT` after them to show the result, and a few extra queries check or extend the required ones.

## How to run

1. Open `hw4_olist.ipynb` in Google Colab.
2. Select **Runtime → Restart session and run all**.

The first cell installs everything that is needed, and the data is downloaded from Kaggle without credentials, so there is nothing to upload or configure. Every section drops and recreates its tables, so repeated runs give the same results; only the `created_at`, `updated_at` and `assigned_at` timestamps change. The notebook works on the current default Colab runtime (Python 3.13) as well as on Python 3.12, and also runs locally. The Windows build of `pgserver` has no time zone database, so there the session uses the equivalent POSIX rule `UTC0` instead of `UTC`; see section 1.1.
