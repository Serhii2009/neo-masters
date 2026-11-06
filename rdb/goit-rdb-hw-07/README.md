# goit-rdb-hw-07

Homework 7 for the Relational Databases course (GoIT Neoversity): time-series ML features over
NYC Taxi data and a semi-structured event log in `JSONB`. The notebook builds lag, rolling and
expanding features with window functions partitioned by pickup zone, stores a synthetic
clickstream as `JSONB`, and measures with `EXPLAIN (ANALYZE, BUFFERS)` what a GIN index and an
expression B-tree index do to the query plans.

**Dataset:** NYC Taxi & Limousine Commission yellow taxi trip records, February and March 2024.
**Stack:** PostgreSQL 16 (via `pgserver`) in Google Colab, SQL cells through `jupysql`.

## Data source

| What | Link |
|---|---|
| Trip records | [TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) |
| Files used | `yellow_tripdata_2024-02.parquet`, `yellow_tripdata_2024-03.parquet` |

## How the data gets into the database

1. Both Parquet files are downloaded straight from the official CloudFront endpoint, which
   needs no credentials, and cached in the system temp directory.
2. The seven columns the task lists are read, the task's cleaning rules are applied
   (`fare_amount` and `trip_distance` within range, `PULocationID` present), and the rows are
   restricted to the February–March window.
3. A reproducible random sample of 500 000 rows is loaded into `nyc_taxi_raw` with
   `pandas.to_sql`, and `t7_hw_taxi_daily` is built from it in SQL.

Parquet and CSV files are not committed; the notebook fetches them.

| Table | Rows |
|---|---|
| `nyc_taxi_raw` | 500,000 |
| `t7_hw_taxi_daily` | 8,623 zone-days over 60 days, 246 zones |
| `v_t7_hw_taxi_features` | 2,968 training rows across 134 zones |
| `t7_hw_events` | 50,000 events, 5 types of 10,000 each |
| `t7_hw_checkouts_norm` | 10,000 |

## Time-series features

All of them are computed per pickup zone, that is with `PARTITION BY pickup_zone_id`.

| Feature | Definition | Window frame |
|---|---|---|
| `trips_lag_1d`, `trips_lag_7d`, `trips_lag_30d` | trip count 1, 7 and 30 rows back | default |
| `rolling_avg_fare_7d` | mean of `avg_fare` over the calendar week to date | `RANGE BETWEEN INTERVAL '6 days' PRECEDING AND CURRENT ROW` |
| `rolling_std_fare_30d` | sample standard deviation of `avg_fare` over 30 days | `RANGE BETWEEN INTERVAL '29 days' PRECEDING AND CURRENT ROW` |
| `cumulative_trips`, `expanding_avg_trips` | running total and running mean | `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` |

`v_t7_hw_taxi_features` combines all of them and keeps only rows with a full 30 days of
history behind them, which is what a training set with complete features looks like.

## The JSONB part

`t7_hw_events` holds five event types whose payload schemas differ: `page_view`, `click`,
`add_to_cart`, `checkout` and `recommendation_shown`. It is queried three ways — containment
with `@>`, top-level key existence with `?` and `?|`, and JSONPath through `jsonb_path_query`
and `jsonb_path_exists`. Section 4 captures four `EXPLAIN (ANALYZE, BUFFERS)` plans: containment
before and after a `jsonb_path_ops` GIN index, and `payload ->> 'device' = 'mobile'` before and
after an expression B-tree index. Section 5 repeats one aggregation against the normalized
`t7_hw_checkouts_norm` table and compares the two plans.

## Repository contents

| File | Description |
|---|---|
| `hw7_taxi_features_jsonb.ipynb` | Main notebook with all five tasks, executed end-to-end with outputs |
| `README.md` | This file |

## Where to find each task in the notebook

| Task | Section | What is there |
|---|---|---|
| 1. Setup and data | 1 | `pgserver` and the PostgreSQL version, the Parquet download, cleaning and sampling, `nyc_taxi_raw`, the daily aggregation, a coverage check, and a `TIMESTAMPTZ` demo table |
| 2. Time-series features | 2 | Lag, rolling 7-day mean, rolling 30-day volatility, expanding totals, the combined view, and a demonstration of what dropping `PARTITION BY` silently does |
| 3. JSONB event log | 3 | `t7_hw_events` with five payload shapes, then containment, key existence and JSONPath queries |
| 4. GIN and EXPLAIN | 4 | Four plans around the GIN and the expression index, with both index sizes |
| 5. JSONB vs normalized | 5 | `t7_hw_checkouts_norm`, the same aggregation both ways, and the MongoDB pipeline as pseudocode |
| Reflection | 6 | Answers tied to the actual costs and timings above |
| Final checks | 7 | Assertions on every result, printing `All checks passed` |

## Changes to the assignment template

- **Two months instead of one, and a random sample instead of `head()`.** The template reads
  `yellow_tripdata_2024-03.parquet` and takes `head(500_000)`. That Parquet file is ordered by
  pickup time, so the first 500 000 rows cover only seven days, 29 February to 6 March. With
  seven days of history `LAG(trip_count, 30)` is `NULL` on every row and the combined feature
  view, which filters `WHERE trips_lag_30d IS NOT NULL`, comes out empty. February and March
  together give 60 days, the horizon the stub fallback in the task is built around, and a
  seeded `sample()` keeps the whole span instead of its first week.
- **An explicit date window.** The March file contains stray pickup timestamps from 2002 and
  from April 2024. Without `WHERE` on the period those rows become their own `ts_day` groups.
- **Time zones are probed, not assumed.** The Windows build of `pgserver` ships without the
  IANA time zone database, so neither `America/New_York` nor plain `UTC` resolves there. The
  notebook tests both and falls back to the equivalent POSIX rules, so it runs on Colab and
  locally without edits. On Colab the named zones are used.
- **`DROP VIEW` before `DROP TABLE`.** `v_t7_hw_taxi_features` depends on `t7_hw_taxi_daily`,
  so a second run on an existing database fails on the plain `DROP TABLE` from the template.
- **`EXPLAIN` runs through a small helper** that prints the plan with its indentation; inside a
  result table the plan tree is unreadable.
- Variant A is used throughout. The stub-schema fallback is not needed.

## How to run

1. Open `hw7_taxi_features_jsonb.ipynb` in Google Colab.
2. Select **Runtime → Restart session and run all**.

The first cell installs everything, and the data comes from the public TLC endpoint without
credentials, so there is nothing to upload. Every section drops and recreates its own objects,
so repeated runs give the same results; only the `EXPLAIN` timings change.
