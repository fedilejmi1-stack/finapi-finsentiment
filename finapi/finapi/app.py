"""Flask application exposing stock price, database and sentiment endpoints."""

from flask import Flask, jsonify, request
from sqlalchemy import func

from finapi.sentiment import analyze_sentiment, analyze_batch
from finapi.db import SessionLocal, init_db
from finapi.models import PriceRecord, NewsItem
from finapi.prices import (
    TickerNotFoundError,
    get_latest_price,
    get_history,
)


def create_app() -> Flask:
    app = Flask(__name__)

    init_db()

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"}), 200

    @app.get("/price/<ticker>")
    def price(ticker: str):
        try:
            latest = get_latest_price(ticker)
        except TickerNotFoundError as e:
            return jsonify({"error": str(e), "code": 404}), 404
        except Exception:
            return jsonify({"error": "Erreur interne", "code": 500}), 500

        return jsonify({
            "ticker": latest.ticker,
            "date": latest.date.isoformat(),
            "close": latest.close,
            "currency": latest.currency,
        })

    @app.get("/history/<ticker>")
    def history(ticker: str):
        raw_days = request.args.get("days", "30")

        try:
            days = int(raw_days)
        except ValueError:
            return jsonify({
                "error": "Le parametre 'days' doit etre un entier",
                "code": 400,
            }), 400

        if not 1 <= days <= 365:
            return jsonify({
                "error": "Le parametre 'days' doit etre entre 1 et 365",
                "code": 400,
            }), 400

        try:
            points = get_history(ticker, days)
        except TickerNotFoundError as e:
            return jsonify({"error": str(e), "code": 404}), 404
        except Exception:
            return jsonify({"error": "Erreur interne", "code": 500}), 500

        return jsonify({
            "ticker": ticker.upper(),
            "days_requested": days,
            "prices": [
                {
                    "date": p.date.isoformat(),
                    "close": p.close,
                }
                for p in points
            ],
        })

    @app.get("/db/prices/<ticker>")
    def db_prices(ticker: str):
        with SessionLocal() as session:
            rows = (
                session.query(PriceRecord)
                .filter(PriceRecord.ticker == ticker.upper())
                .order_by(PriceRecord.date.desc())
                .limit(100)
                .all()
            )

        return jsonify({
            "ticker": ticker.upper(),
            "count": len(rows),
            "prices": [
                {
                    "date": r.date.isoformat(),
                    "close": r.close,
                }
                for r in rows
            ],
        })

    @app.get("/db/news/<ticker>")
    def db_news(ticker: str):
        with SessionLocal() as session:
            rows = (
                session.query(NewsItem)
                .filter(NewsItem.ticker == ticker.upper())
                .order_by(NewsItem.published_at.desc())
                .limit(20)
                .all()
            )

        return jsonify({
            "ticker": ticker.upper(),
            "count": len(rows),
            "news": [
                {
                    "published_at": r.published_at.isoformat(),
                    "title": r.title,
                    "publisher": r.publisher,
                    "url": r.url,
                    "sentiment_label": r.sentiment_label,
                    "sentiment_score": r.sentiment_score,
                }
                for r in rows
            ],
        })

    @app.post("/sentiment")
    def sentiment():
        data = request.get_json(silent=True)

        if not data or "text" not in data:
            return jsonify({
                "error": "Missing 'text' field",
                "code": 400,
            }), 400

        result = analyze_sentiment(data["text"])

        return jsonify(result), 200

    @app.post("/sentiment/batch")
    def sentiment_batch():
        data = request.get_json(silent=True)

        if not data or "texts" not in data:
            return jsonify({
                "error": "Missing 'texts' field",
                "code": 400,
            }), 400

        texts = data["texts"]

        if not isinstance(texts, list):
            return jsonify({
                "error": "'texts' must be a list",
                "code": 400,
            }), 400

        if len(texts) == 0:
            return jsonify({
                "error": "'texts' cannot be empty",
                "code": 400,
            }), 400

        if len(texts) > 100:
            return jsonify({
                "error": "Maximum 100 texts per request",
                "code": 400,
            }), 400

        results = analyze_batch(texts)

        return jsonify({
            "count": len(results),
            "results": results,
        }), 200

    @app.get("/db/sentiment-summary/<ticker>")
    def sentiment_summary(ticker: str):
        with SessionLocal() as session:
            rows = (
                session.query(
                    NewsItem.sentiment_label,
                    func.count(NewsItem.id)
                )
                .filter(NewsItem.ticker == ticker.upper())
                .filter(NewsItem.sentiment_label.isnot(None))
                .group_by(NewsItem.sentiment_label)
                .all()
            )

        return jsonify({
            "ticker": ticker.upper(),
            "summary": {
                label: count
                for label, count in rows
            },
        })

    return app


if __name__ == "__main__":
    create_app().run(debug=True, port=5000)