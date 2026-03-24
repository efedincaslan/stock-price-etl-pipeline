# Stock Price ETL Pipeline

A end-to-end data engineering project built to understand the ETL process through 
a real-world use case — ingesting live stock market data, transforming it into a 
structured format, and loading it into a PostgreSQL database on a daily schedule.

## Overview

This pipeline connects to the [Alpha Vantage API](https://www.alphavantage.co/) to 
pull daily stock price data for multiple tickers. It extracts raw JSON, transforms 
it into a clean, typed DataFrame, and loads it into a Postgres database using an 
upsert strategy to prevent duplicates. The pipeline is orchestrated with Apache 
Airflow running in Docker and is scheduled to run daily.

## Tech Stack

- **Python** — core pipeline logic (requests, pandas, sqlalchemy)
- **PostgreSQL** — data storage (managed via DBeaver)
- **Apache Airflow** — orchestration and scheduling
- **Docker** — containerization for Airflow
- **Alpha Vantage API** — stock market data source

## Architecture
```
Alpha Vantage API
       ↓
   extract.py        → Fetches daily OHLCV data, caches response to JSON
       ↓
  transform.py       → Cleans types, renames columns, sorts by date
       ↓
    load.py          → Upserts into PostgreSQL (conflict on date + symbol)
       ↓
  PostgreSQL DB      → ibm_data.stock_prices (composite PK: date + symbol)
       ↓
Airflow DAG          → Scheduled daily via Docker
```

## Database Schema
```sql
CREATE TABLE ibm_data.stock_prices (
    date     DATE        NOT NULL,
    symbol   VARCHAR     NOT NULL,
    open     NUMERIC     NOT NULL,
    high     NUMERIC     NOT NULL,
    low      NUMERIC     NOT NULL,
    close    NUMERIC     NOT NULL,
    volume   BIGINT      NOT NULL,
    PRIMARY KEY (date, symbol)
);
```

## Features

- **Multi-ticker support** — configure any number of symbols via `config.py`
- **Smart caching** — API responses are cached as JSON with a freshness check, 
  so the API is only called once per day per ticker
- **Rate limiting** — 12 second delay between API calls to respect free tier limits
- **Upsert logic** — duplicate rows are silently skipped on re-runs
- **Logging** — structured logging across all pipeline stages
- **Airflow DAG** — daily schedule with full run history and task visibility

## How to Run

### Prerequisites
- Docker Desktop
- PostgreSQL (local instance)
- Alpha Vantage API key (free tier at alphavantage.co)

### Setup

1. Clone the repo
```bash
   git clone https://github.com/efedincaslan/stock-price-etl-pipeline.git
   cd stock-price-etl-pipeline
```

2. Create a `.env` file in `airflow/dags/` with your credentials:
```
   ALPHA_VANTAGE_KEY=your_api_key
   DB_USER=your_postgres_user
   DB_PASS=your_postgres_password
```

3. Add your desired tickers to `airflow/dags/config.py`:
```python
   SYMBOLS = ['AAPL', 'IBM', 'MSFT']
```

4. Start Airflow:
```bash
   cd airflow
   docker-compose up -d
```

5. Open the Airflow UI at `http://localhost:8080` and trigger the `stock_pipeline` DAG.

## Notes

- The pipeline requires Docker to be running for the Airflow scheduler to execute. 
  For full automation, this would be deployed to a cloud environment (AWS EC2, 
  Google Cloud Composer, or AWS MWAA).
- The free Alpha Vantage tier allows 25 requests per day. If the daily limit is 
  reached, the pipeline falls back to the cached JSON from the previous run.

## What I Learned

- Designing and building a modular ETL pipeline from scratch
- Schema design with composite primary keys and upsert conflict handling
- API ingestion with rate limiting and response validation
- Containerizing a workflow with Docker and Apache Airflow
- Debugging multi-symbol pipeline failures and refactoring for scalability
