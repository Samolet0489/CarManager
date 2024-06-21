import pytest
from src.app import create_app
from src.database import db
from src.model.vehicle import Vehicle

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
