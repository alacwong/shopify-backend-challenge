from . import client
from blueprints.images.util.fuzzy_string_matcher import get_closest_string


def test_root_url(client):
    response = client.get('/')
    assert response.status_code == 404
    assert response.json == {"description": "Not Found"}


def test_closest_word():
    """
    Test fuzzy string matcher
    """
    pokemon = get_closest_string('charminder')
    assert pokemon == 'Charmander'


def test_search_endpoint(client):
    """
    Test text search endpoint
    """

    response = client.get("/images/search?pokemon=Abra")
    for res in response:
        assert res.tag == 'Abra'

