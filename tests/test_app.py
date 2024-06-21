import pytest
from src.app import create_app
from src.database import db
from src.model.vehicle import Vehicle
from src.model.mechanic import Mechanic

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

def test_get_vehicles(client):
    response = client.get('/vehicles')
    assert response.status_code == 200
    assert b"vehicle-card" in response.data or b"No vehicles" in response.data

def test_create_vehicle(client, app):
    vehicle_data = {
        'name': 'Test Car',
        'color': 'Blue',
        'expenses': 1000.0,
        'mileage': 10000,
        'note': 'Test Note'
    }
    response = client.post('/save-vehicle', json=vehicle_data)
    assert response.status_code == 200

    with app.app_context():
        vehicle = Vehicle.query.filter_by(name='Test Car').first()
        assert vehicle is not None
        assert vehicle.name == 'Test Car'
        assert vehicle.color == 'Blue'
        assert vehicle.expenses == 1000.0
        assert vehicle.mileage == 10000
        assert vehicle.note == 'Test Note'

def test_update_vehicle(client, app):
    vehicle_data = {
        'name': 'Test Car',
        'color': 'Blue',
        'expenses': 1000.0,
        'mileage': 10000,
        'note': 'Test Note'
    }
    client.post('/save-vehicle', json=vehicle_data)

    updated_vehicle_data = {
        'name': 'Test Car',
        'color': 'Red',
        'expenses': 1500.0,
        'mileage': 15000,
        'note': 'Updated Test Note'
    }
    response = client.post('/save-vehicle', json=updated_vehicle_data)
    assert response.status_code == 200

    with app.app_context():
        vehicle = Vehicle.query.filter_by(name='Test Car').first()
        assert vehicle is not None
        assert vehicle.color == 'Red'
        assert vehicle.expenses == 1500.0
        assert vehicle.mileage == 15000
        assert vehicle.note == 'Updated Test Note'

def test_get_mechanics(client):
    response = client.get('/mechanics')
    assert response.status_code == 200
    assert b"mechanics-table" in response.data or b"No mechanics" in response.data

def test_create_mechanic(client, app):
    mechanic_data = {
        'name': 'Test Mechanic',
        'address': '123 Test Street',
        'email': 'test@mechanic.com',
        'phone': '1234567890',
        'hourly_rate': 50.0,
        'note': 'Test Note'
    }
    response = client.post('/save_mechanic', json=mechanic_data)
    assert response.status_code == 200

    with app.app_context():
        mechanic = Mechanic.query.filter_by(name='Test Mechanic').first()
        assert mechanic is not None
        assert mechanic.name == 'Test Mechanic'
        assert mechanic.address == '123 Test Street'
        assert mechanic.email == 'test@mechanic.com'
        assert mechanic.phone == '1234567890'
        assert mechanic.hourly_rate == 50.0
        assert mechanic.note == 'Test Note'

def test_update_mechanic(client, app):
    mechanic_data = {
        'name': 'Test Mechanic',
        'address': '123 Test Street',
        'email': 'test@mechanic.com',
        'phone': '1234567890',
        'hourly_rate': 50.0,
        'note': 'Test Note'
    }
    client.post('/save_mechanic', json=mechanic_data)

    updated_mechanic_data = {
        'name': 'Test Mechanic',
        'address': '456 Updated Street',
        'email': 'updated@mechanic.com',
        'phone': '0987654321',
        'hourly_rate': 75.0,
        'note': 'Updated Test Note'
    }
    response = client.post('/save_mechanic', json=updated_mechanic_data)
    assert response.status_code == 200

    with app.app_context():
        mechanic = Mechanic.query.filter_by(name='Test Mechanic').first()
        assert mechanic is not None
        assert mechanic.address == '456 Updated Street'
        assert mechanic.email == 'updated@mechanic.com'
        assert mechanic.phone == '0987654321'
        assert mechanic.hourly_rate == 75.0
        assert mechanic.note == 'Updated Test Note'
