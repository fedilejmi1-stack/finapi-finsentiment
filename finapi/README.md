# FinAPI

A Flask-based financial API that provides stock prices, historical data, news ingestion, and AI-powered sentiment analysis using FinBERT.

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

Windows (Git Bash):

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

# Run the API

```bash
python -m finapi.app
```

The API is available at:

```
http://127.0.0.1:5000
```

---

# API Endpoints

## Health

```
GET /health
```

---

## Latest Price

```
GET /price/<ticker>
```

Example:

```
GET /price/AAPL
```

---

## Historical Prices

```
GET /history/<ticker>?days=30
```

Example:

```
GET /history/AAPL?days=30
```

---

## Prices Stored in Database

```
GET /db/prices/<ticker>
```

Example:

```
GET /db/prices/AAPL
```

---

## News Stored in Database

```
GET /db/news/<ticker>
```

Example:

```
GET /db/news/AAPL
```

---

## Sentiment Analysis

```
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

```
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

```
GET /db/sentiment-summary/<ticker>
```

Example:

```
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

(The exact numbers depend on the news currently available from Yahoo Finance.)

---

# Technologies

* Python 3
* Flask
* SQLAlchemy
* SQLite
* yfinance
* Transformers
* FinBERT (ProsusAI/finbert)

---

# Project Structure

```
finapi/
│
├── data/
│   └── finapi.db
│
├── finapi/
│   ├── app.py
│   ├── db.py
│   ├── models.py
│   ├── prices.py
│   ├── sentiment.py
│   └── etl/
│
├── scripts/
│   ├── run_etl.py
│   └── enrich_sentiment.py
│
├── tests/
├── requirements.txt
└── README.md
```
