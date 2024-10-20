import itertools

import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_state():
    app.state.matches.clear()
    app.state.id_generator = itertools.count(1)


@pytest.fixture
def create_test_matches():
    match_data_1 = {
        "home_team": "Волки",
        "away_team": "Быки",
        "home_score": 2,
        "away_score": 5,
        "match_date": "2024-10-19",
        "place": "Лесная опушка",
        "duration": 92,
        "yellow_cards": 3,
        "red_cards": 0,
    }
    match_data_2 = {
        "home_team": "Кошки",
        "away_team": "Собаки",
        "home_score": 1,
        "away_score": 1,
        "match_date": "2024-10-20",
        "place": "Коридор",
        "duration": 93,
        "yellow_cards": 2,
        "red_cards": 1,
    }
    client.post("/matches/", json=match_data_1)
    client.post("/matches/", json=match_data_2)


def test_get_all_matches(create_test_matches):
    response = client.get("/matches/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["home_team"] == "Волки"
    assert data[1]["home_team"] == "Кошки"


def test_get_match_by_id(create_test_matches):
    response = client.get("/matches/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["home_team"] == "Волки"
    assert data["away_team"] == "Быки"


def test_stats(create_test_matches):
    response = client.get("/matches/stats/?field=home_score")
    assert response.status_code == 200
    data = response.json()
    assert data["average"] == 1.5
    assert data["max"] == 2
    assert data["min"] == 1


def test_delete_match(create_test_matches):
    response = client.delete("/matches/1")
    assert response.status_code == 200
    data = response.json()
    assert data["detail"] == "Match deleted"
    response = client.get("/matches/1")
    assert response.status_code == 404
