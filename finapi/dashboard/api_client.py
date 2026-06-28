"""Embedded backend client for Hugging Face Spaces deployment.

Instead of calling the Flask API over HTTP, the Streamlit dashboard
queries the database directly. This keeps the deployment single-process.
"""

from sqlalchemy import func

from finapi.db import SessionLocal, init_db
from finapi.models import NewsItem, PriceRecord


def get_health() -> bool:
    """Return True when the embedded backend is available."""
    try:
        init_db()
        return True
    except Exception:
        return False


def get_db_stats() -> dict:
    """Return basic database statistics."""
    init_db()

    with SessionLocal() as session:
        prices_count = session.query(PriceRecord).count()
        news_count = session.query(NewsItem).count()
        news_enriched = (
            session.query(NewsItem)
            .filter(NewsItem.sentiment_label.isnot(None))
            .count()
        )

        tickers = sorted({
            ticker
            for (ticker,) in session.query(PriceRecord.ticker).distinct().all()
        })

    return {
        "prices_count": prices_count,
        "news_count": news_count,
        "news_enriched": news_enriched,
        "tickers": tickers,
    }


def get_db_prices(ticker: str) -> list[dict]:
    """Return latest stored prices for a ticker."""
    init_db()

    with SessionLocal() as session:
        rows = (
            session.query(PriceRecord)
            .filter(PriceRecord.ticker == ticker.upper())
            .order_by(PriceRecord.date.desc())
            .limit(100)
            .all()
        )

    return [
        {
            "date": row.date.isoformat(),
            "close": row.close,
            "currency": row.currency,
        }
        for row in rows
    ]


def get_db_news(ticker: str) -> list[dict]:
    """Return latest stored news for a ticker."""
    init_db()

    with SessionLocal() as session:
        rows = (
            session.query(NewsItem)
            .filter(NewsItem.ticker == ticker.upper())
            .order_by(NewsItem.published_at.desc())
            .limit(20)
            .all()
        )

    return [
        {
            "published_at": row.published_at.isoformat(),
            "title": row.title,
            "publisher": row.publisher,
            "url": row.url,
            "summary": row.summary,
            "sentiment_label": row.sentiment_label,
            "sentiment_score": row.sentiment_score,
        }
        for row in rows
    ]


def get_sentiment_summary(ticker: str) -> dict[str, int]:
    """Return sentiment distribution for a ticker."""
    init_db()

    with SessionLocal() as session:
        rows = (
            session.query(NewsItem.sentiment_label, func.count(NewsItem.id))
            .filter(NewsItem.ticker == ticker.upper())
            .filter(NewsItem.sentiment_label.isnot(None))
            .group_by(NewsItem.sentiment_label)
            .all()
        )

    return {label: count for label, count in rows}