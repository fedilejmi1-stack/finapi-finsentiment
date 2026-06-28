"""Shared pytest fixtures."""

import pytest

from finapi.app import create_app


@pytest.fixture
def client():
    """Create a Flask test client."""
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()
