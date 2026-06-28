---
title: FinSentiment
emoji: 📈
colorFrom: blue
colorTo: yellow
sdk: streamlit
sdk_version: 1.30.0
app_file: app.py
pinned: false
license: mit
---

# FinAPI
![CI](https://github.com/fedilejmi1-stack/finapi-finsentiment/actions/workflows/ci.yml/badge.svg)

A Flask-based financial API that provides stock prices, historical data, news ingestion, AI-powered sentiment analysis using FinBERT, and an interactive Streamlit dashboard.

---

## Features

### Lab 1

* Health check endpoint
* Latest stock price endpoint
* Historical price endpoint
* Error handling

### Lab 2

* SQLite database with SQLAlchemy
* ETL pipeline for prices
* ETL pipeline for financial news
* Database API endpoints

### Lab 3

* FinBERT sentiment analysis
* Batch sentiment analysis
* News sentiment enrichment
* Sentiment summary endpoint
* Singleton model loading using `lru_cache`

### Lab 4

* Interactive Streamlit dashboard
* Sidebar ticker selector
* Price metrics
* Plotly price chart
* Sentiment distribution chart
* Colored news list by sentiment
* Cached API calls using `@st.cache_data`

### Lab 5

* Automated tests with pytest
* Coverage reporting with pytest-cov
* Ruff linting and formatting
* GitHub Actions CI workflow
* CI badge in README
* Pull Request workflow

---

---

# Installation

Clone the repository:

```bash
git clone <repository_url>
cd finapi
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it.

Windows Git Bash:

```bash
source .venv/Scripts/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Initialize the Database

```bash
python -c "from finapi.db import init_db; init_db()"
```

---

# ETL Pipeline

Load prices and news:

```bash
PYTHONPATH=. python scripts/run_etl.py AAPL MSFT GOOGL
```

Enrich news with FinBERT sentiment:

```bash
PYTHONPATH=. python scripts/enrich_sentiment.py
```

---

# Run the Flask API

Run the API from the project root:

```bash
python -m finapi.app
```

The API is available at:

```text
http://127.0.0.1:5000
```

---

# Run the Streamlit Dashboard

The Flask API must be running before launching the dashboard.

## Terminal 1 — Start the Flask API

```bash
cd finapi
source .venv/Scripts/activate
python -m finapi.app
```

## Terminal 2 — Start the Streamlit dashboard

```bash
cd finapi
source .venv/Scripts/activate
streamlit run dashboard/app.py
```

The dashboard is available at:

```text
http://localhost:8501
```

---

# API Endpoints

## Health

```text
GET /health
```

---

## Latest Price

```text
GET /price/<ticker>
```

Example:

```text
GET /price/AAPL
```

---

## Historical Prices

```text
GET /history/<ticker>?days=30
```

Example:

```text
GET /history/AAPL?days=30
```

---

## Prices Stored in Database

```text
GET /db/prices/<ticker>
```

Example:

```text
GET /db/prices/AAPL
```

---

## News Stored in Database

```text
GET /db/news/<ticker>
```

Example:

```text
GET /db/news/AAPL
```

---

## Sentiment Analysis

```text
POST /sentiment
```

Example body:

```json
{
  "text": "Apple reported record profits this quarter."
}
```

---

## Batch Sentiment Analysis

```text
POST /sentiment/batch
```

Example body:

```json
{
  "texts": [
    "Apple reported record profits.",
    "Tesla missed expectations.",
    "The Fed kept rates unchanged."
  ]
}
```

---

## Sentiment Summary

```text
GET /db/sentiment-summary/<ticker>
```

Example:

```text
GET /db/sentiment-summary/AAPL
```

Example response:

```json
{
  "ticker": "AAPL",
  "summary": {
    "positive": 13,
    "neutral": 8,
    "negative": 3
  }
}
```

The exact numbers depend on the news currently available from Yahoo Finance and the articles stored in the database.

---

# Dashboard Features

The Streamlit dashboard includes:

* A sidebar to select the ticker
* Four main metrics:

  * Last close
  * Date
  * Stored news
  * Positive sentiment percentage
* An interactive Plotly line chart for price evolution
* A sentiment distribution pie chart
* A colored list of latest news by sentiment
* Cached API calls using `@st.cache_data`

---

# Screenshots

Dashboard screenshots should be saved in:

```text
docs/screenshots/
```

Example:

```text
docs/screenshots/lab4_dashboard.png
```

---

# Technologies

* Python 3
* Flask
* SQLAlchemy
* SQLite
* yfinance
* Transformers
* FinBERT `ProsusAI/finbert`
* Streamlit
* Plotly
* Requests

---

# Project Structure

```text
finapi/
│
├── data/
│   └── finapi.db
│
├── dashboard/
│   ├── __init__.py
│   ├── app.py
│   ├── api_client.py
│   └── charts.py
│
├── docs/
│   └── screenshots/
│       └── lab4_dashboard.png
│
├── finapi/
│   ├── __init__.py
│   ├── app.py
│   ├── db.py
│   ├── models.py
│   ├── prices.py
│   ├── sentiment.py
│   └── etl/
│       ├── __init__.py
│       ├── prices_etl.py
│       └── news_etl.py
│
├── scripts/
│   ├── run_etl.py
│   └── enrich_sentiment.py
│
├── tests/
│   └── test_app.py
│
├── requirements.txt
└── README.md
```

---

# Git History

The project is organized by lab commits:

```text
Lab 0: setup verification
Lab 1: API Flask pour cours boursiers
Lab 2: SQLite database and ETL pipeline
Lab 2: SQLite database, ETL and DB endpoints
Lab 3: FinBERT sentiment analysis
Lab 3: FinBERT sentiment analysis and news enrichment
Lab 4: add Streamlit dashboard
```
