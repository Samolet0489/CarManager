import pytest
from src.app import create_app
from src.database import db
from src.model.mechanic import Mechanic
from src.api.mechanicG import mechanic_api

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def init_mechanic(app):
    with app.app_context():
        mechanic = Mechanic(id=1, name="Test Mechanic", address="123 Test Street", email="test@mechanic.com", phone="1234567890", hourly_rate=50.0, note="Test Note")
        db.session.add(mechanic)
        db.session.commit()
        yield mechanic

def test_create_mechanic(client):
    mechanic_data = {
        "name": "New Mechanic",
        "address": "456 New Street",
        "email": "new@mechanic.com",
        "phone": "0987654321",
        "hourly_rate": 75.0,
        "note": "New note"
    }
    response = client.post('/mechanic/', json=mechanic_data)
    assert response.status_code == 201
    response_json = response.get_json()
    assert response_json['mechanic']['name'] == "New Mechanic"
    assert response_json['mechanic']['address'] == "456 New Street"
    assert response_json['mechanic']['email'] == "new@mechanic.com"
    assert response_json['mechanic']['phone'] == "0987654321"
    assert response_json['mechanic']['hourly_rate'] == 75.0
    assert response_json['mechanic']['note'] == "New note"

def test_get_mechanics(client, init_mechanic):
    response = client.get('/mechanic/')
    assert response.status_code == 200
    response_json = response.get_json()
    assert len(response_json) == 1
    assert response_json[0]['name'] == "Test Mechanic"
    assert response_json[0]['address'] == "123 Test Street"
    assert response_json[0]['email'] == "test@mechanic.com"
    assert response_json[0]['phone'] == "1234567890"
    assert response_json[0]['hourly_rate'] == 50.0
    assert response_json[0]['note'] == "Test Note"

def test_delete_mechanic(client, init_mechanic):
    response = client.delete('/mechanic/', query_string={'id': 1})
    assert response.status_code == 204

    response = client.get('/mechanic/')
    assert response.status_code == 200
    response_json = response.get_json()
    assert len(response_json) == 0
