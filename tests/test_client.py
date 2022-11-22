from http import HTTPStatus
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

body = {
  "url": "string"
}

batch_upload = [
    {"url": "string"},
    {"url": "string2"}
]


def test_get_db_status():
    response = client.get('api/ping')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'DB connection': 'Access established'}


def test_get_status_url():
    response = client.get('/111NNN/status')
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_get_url():
    response = client.get('/111NNN/status')
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_short_url():
    response = client.post('/api/url', json=body)
    result = response.json()
    assert result.get('url') == 'string'


def test_batch_upload():
    response = client.post('api/shorten', json=batch_upload)
    result = response.json()
    assert len(result) == 2
    assert result[1].get('url') == 'string2'
