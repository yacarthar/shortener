import pytest
from flask import current_app

from main import app


@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            assert current_app.config["FLASK_ENV"] == "development"
        yield client


def test_index_page(client):
   response = client.get('/')

   assert response.status_code == 200
   assert b'hello' in response.data