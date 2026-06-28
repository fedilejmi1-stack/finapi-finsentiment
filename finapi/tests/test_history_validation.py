"""Tests for history endpoint validation."""


def test_history_rejects_non_integer_days(client):
    response = client.get("/history/AAPL?days=abc")
    data = response.get_json()

    assert response.status_code == 400
    assert data["code"] == 400
    assert "days" in data["error"]


def test_history_rejects_days_too_low(client):
    response = client.get("/history/AAPL?days=0")
    data = response.get_json()

    assert response.status_code == 400
    assert data["code"] == 400
    assert "entre 1 et 365" in data["error"]


def test_history_rejects_days_too_high(client):
    response = client.get("/history/AAPL?days=999")
    data = response.get_json()

    assert response.status_code == 400
    assert data["code"] == 400
    assert "entre 1 et 365" in data["error"]
