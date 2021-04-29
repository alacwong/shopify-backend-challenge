from . import client
from blueprints.images.util.errors import INVALID_QUERY


def test_root_url(client):
    response = client.get('/')
    assert response.status_code == 404
    assert response.json == {"description": "Not Found"}


def test_fuzzy_search(client):
    """
    Test fuzzy string matcher
    """
    response = client.get("/images/search?pokemon=charminder")
    json = response.json
    for image in json:
        assert image['tag'] == 'Charmander'


def test_search_endpoint(client):
    """
    Test text search endpoint
    """

    response = client.get("/images/search?pokemon=Abra")
    json = response.json
    for image in json:
        assert image['tag'] == 'Abra'


def test_invalid_query(client):
    """
    Test invalid query
    """
    response = client.get("/images/search?pokemon=Abra&page=-1")
    assert response.status_code == 400
    assert response.json == INVALID_QUERY
