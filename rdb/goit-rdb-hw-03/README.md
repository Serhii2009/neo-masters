# goit-rdb-hw-03

Homework 3 for the Relational Databases course (GoIT Neoversity): turning a raw file into an analysis-ready PostgreSQL table, with a staging layer, typed DDL, a data-quality audit and EDA in SQL.

**Dataset:** NYC TLC Yellow Taxi Trip Records, March 2024.
**Stack:** PostgreSQL 16 (via `pgserver`) in Google Colab, SQL cells via `jupysql`.

## Data source

| What | Link |
|---|---|
| Official page | [NYC TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) |
| Trip file | [`yellow_tripdata_2024-03.parquet`](https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-03.parquet) (about 60 MB, 3,582,628 rows, 19 columns) |
| Zone lookup | [`taxi_zone_lookup.csv`](https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv) (265 zones) |
| Field definitions | [Data dictionary, yellow taxi](https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf) |

## How the sample was built

1. The notebook downloads the monthly Parquet file and keeps 15 of its 19 columns: time, zones, distance, rate code, payment, fare, tip, total, congestion surcharge and airport fee.
2. It draws a seeded random sample of **100,000 trip keys** (`random_state=42`). A trip key is vendor + pickup time + dropoff time + pickup zone + dropoff zone. All records of a sampled key are kept, because TLC stores corrections as a second record with the same key and negated amounts. Sampling single rows would split those pairs.
3. The result is written to `data/hw3_taxi_sample.csv` (**101,102 rows**, 9 MB) and loaded into PostgreSQL with `COPY FROM STDIN`.

A random sample is used instead of `head()` because the file is ordered by time, so the first 100,000 rows would only cover March 1.

| Layer | Table | Rows |
|---|---|---|
| Raw (all `TEXT`) | `hw3_taxi_staging` | 101,102 |
| Reference | `hw3_taxi_zones` | 265 |
| Typed, cleaned | `hw3_taxi_trips` | 101,099 |

Three rows were excluded because their dropoff is recorded before their pickup.

## Repository contents

| File | Description |
|---|---|
| `hw3_nyc_taxi.ipynb` | Main notebook with all six tasks, executed end-to-end with outputs |
| `data/hw3_taxi_sample.csv` | The controlled CSV sample that is loaded via `COPY` |
| `data/taxi_zone_lookup.csv` | Official TLC zone lookup |

## Where to find each task in the notebook

| Task | Section | What is there |
|---|---|---|
| 1. Setup and loading | 1 | `pgserver` start and PostgreSQL version, download and sampling, staging table, `COPY FROM STDIN`, row count, zone lookup |
| 2. Staging and DDL | 2 | Column-by-column type decisions, typed table with PK, FK, `NOT NULL` and 7 `CHECK` constraints, `INSERT INTO ... SELECT` with cleaning, a DST example showing why `TIMESTAMPTZ` is needed |
| 3. Data-quality audit | 3 | Staging vs. clean row counts with the exclusion rule, duplicates on a business key (reversal pairs), NULL rates, raw marker scan, numeric sentinels per vendor |
| 4. Distributions and anomalies | 4 | Payment type distribution, fare and distance statistics, domain outlier check with an action for each rule |
| 5. Ten DQL/EDA queries | 5 | Q1–Q10 as business question / SQL / interpretation, plus a coverage table of the required constructs |
| 6. Reflection | 6 | Data quality, features, leakage, pipeline improvements, ML task |

Section 7 runs assertions on the main requirements and prints `All checks passed`.

## How to run

1. Open `hw3_nyc_taxi.ipynb` in Google Colab.
2. Select **Runtime → Restart session and run all**.

The first cell installs everything that is needed. The notebook downloads the data from the official source and rebuilds the same CSV on every run, so there are no files to upload manually. It works on the current default Colab runtime (Python 3.13) as well as on Python 3.12, and also runs locally on Windows. The Windows build of `pgserver` has no time zone database, so there the notebook uses the equivalent POSIX rule for New York time; see section 1.1.
