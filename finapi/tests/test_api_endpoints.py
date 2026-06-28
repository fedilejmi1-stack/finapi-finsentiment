"""Additional endpoint tests with mocks."""

from datetime import date
from types import SimpleNamespace
from unittest.mock import patch

from finapi.prices import TickerNotFoundError


def test_price_endpoint_success(client):
    fake_price = SimpleNamespace(
        ticker="AAPL",
        date=date(2026, 1, 1),
        close=123.45,
        currency="USD",
    )

    with patch("finapi.app.get_latest_price", return_value=fake_price):
        response = client.get("/price/AAPL")

    data = response.get_json()

    assert response.status_code == 200
    assert data["ticker"] == "AAPL"
    assert data["close"] == 123.45
    assert data["currency"] == "USD"


def test_price_endpoint_ticker_not_found(client):
    with patch(
        "finapi.app.get_latest_price",
        side_effect=TickerNotFoundError("Ticker not found"),
    ):
        response = client.get("/price/INVALID")

    data = response.get_json()

    assert response.status_code == 404
    assert data["code"] == 404
    assert "Ticker not found" in data["error"]


def test_history_endpoint_success(client):
    fake_points = [
        SimpleNamespace(date=date(2026, 1, 1), close=100.0),
        SimpleNamespace(date=date(2026, 1, 2), close=101.5),
    ]

    with patch("finapi.app.get_history", return_value=fake_points):
        response = client.get("/history/AAPL?days=2")

    data = response.get_json()

    assert response.status_code == 200
    assert data["ticker"] == "AAPL"
    assert data["days_requested"] == 2
    assert len(data["prices"]) == 2


def test_sentiment_endpoint_success(client):
    with patch(
        "finapi.app.analyze_sentiment",
        return_value={"label": "positive", "score": 0.95},
    ):
        response = client.post(
            "/sentiment",
            json={"text": "Apple beats expectations"},
        )

    data = response.get_json()

    assert response.status_code == 200
    assert data["label"] == "positive"
    assert data["score"] == 0.95


def test_sentiment_endpoint_missing_text(client):
    response = client.post("/sentiment", json={})
    data = response.get_json()

    assert response.status_code == 400
    assert data["code"] == 400
    assert "text" in data["error"]


def test_sentiment_batch_endpoint_success(client):
    fake_results = [
        {"label": "positive", "score": 0.91, "text_preview": "Apple"},
        {"label": "negative", "score": 0.88, "text_preview": "Tesla"},
    ]

    with patch("finapi.app.analyze_batch", return_value=fake_results):
        response = client.post(
            "/sentiment/batch",
            json={"texts": ["Apple beats expectations", "Tesla misses estimates"]},
        )

    data = response.get_json()

    assert response.status_code == 200
    assert data["count"] == 2
    assert data["results"][0]["label"] == "positive"
    assert data["results"][1]["label"] == "negative"


def test_sentiment_batch_rejects_empty_list(client):
    response = client.post("/sentiment/batch", json={"texts": []})
    data = response.get_json()

    assert response.status_code == 400
    assert data["code"] == 400
