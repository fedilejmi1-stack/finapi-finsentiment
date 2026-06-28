"""Tests for FinBERT sentiment module."""

from unittest.mock import patch

from finapi.sentiment import analyze_batch, analyze_sentiment


@patch("finapi.sentiment.get_classifier")
def test_analyze_sentiment_positive(mock_classifier):
    mock_classifier.return_value = lambda text: [{"label": "positive", "score": 0.95}]

    result = analyze_sentiment("Apple beats expectations")

    assert result["label"] == "positive"
    assert result["score"] == 0.95


@patch("finapi.sentiment.get_classifier")
def test_analyze_batch_returns_results(mock_classifier):
    mock_classifier.return_value = lambda texts, batch_size=16: [
        {"label": "positive", "score": 0.91},
        {"label": "negative", "score": 0.87},
    ]

    result = analyze_batch(
        [
            "Apple beats expectations",
            "Tesla misses estimates",
        ]
    )

    assert len(result) == 2
    assert result[0]["label"] == "positive"
    assert result[1]["label"] == "negative"
    assert result[0]["score"] == 0.91
    assert result[1]["score"] == 0.87
