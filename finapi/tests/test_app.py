"""Additional API endpoint tests."""


def test_sentiment_summary_endpoint_returns_json(client):
    response = client.get("/db/sentiment-summary/AAPL")
    data = response.get_json()

    assert response.status_code == 200
    assert data["ticker"] == "AAPL"
    assert "summary" in data
    assert isinstance(data["summary"], dict)
