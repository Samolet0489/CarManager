import pytest
from src.app import create_app
from src.database import db
from src.model.vehicle import Vehicle
from src.api.vehicleG import vehicle_api

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
def init_vehicle(app):
    with app.app_context():
        vehicle = Vehicle(id=1, name="Test Car", color="Red", expenses=1000.0, mileage=10000, note="Test Note")
        db.session.add(vehicle)
        db.session.commit()
        yield vehicle

def test_create_vehicle(client):
    vehicle_data = {
        "name": "New Car",
        "color": "Blue",
        "expenses": 1500.0,
        "mileage": 5000,
        "note": "Brand new car"
    }
    response = client.post('/vehicle/', json=vehicle_data)
    assert response.status_code == 201
    response_json = response.get_json()
    assert response_json['vehicle']['name'] == "New Car"
    assert response_json['vehicle']['color'] == "Blue"
    assert response_json['vehicle']['expenses'] == 1500.0
    assert response_json['vehicle']['mileage'] == 5000
    assert response_json['vehicle']['note'] == "Brand new car"

def test_get_vehicles(client, init_vehicle):
    response = client.get('/vehicle/')
    assert response.status_code == 200
    response_json = response.get_json()
    assert len(response_json['vehicle']) == 1
    assert response_json['vehicle'][0]['name'] == "Test Car"
    assert response_json['vehicle'][0]['color'] == "Red"
    assert response_json['vehicle'][0]['expenses'] == 1000.0
    assert response_json['vehicle'][0]['mileage'] == 10000
    assert response_json['vehicle'][0]['note'] == "Test Note"

def test_delete_vehicle(client, init_vehicle):
    response = client.delete('/vehicle/', query_string={'id': 1})
    assert response.status_code == 204

    response = client.get('/vehicle/')
    assert response.status_code == 200
    response_json = response.get_json()
    assert len(response_json['vehicle']) == 0

def test_edit_vehicle(client, init_vehicle):
    edit_data = {
        "name": "Updated Car",
        "color": "Green",
        "expenses": 2000.0,
        "mileage": 12000,
        "note": "Updated note"
    }
    response = client.put('/vehicle/', json=edit_data, query_string={'id': 1})
    assert response.status_code == 200

    response = client.get('/vehicle/')
    assert response.status_code == 200
    response_json = response.get_json()
    assert len(response_json['vehicle']) == 1
    assert response_json['vehicle'][0]['name'] == "Updated Car"
    assert response_json['vehicle'][0]['color'] == "Green"
    assert response_json['vehicle'][0]['expenses'] == 2000.0
    assert response_json['vehicle'][0]['mileage'] == 12000
    assert response_json['vehicle'][0]['note'] == "Updated note"
