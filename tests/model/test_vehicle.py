import pytest
from src.app import create_app
from src.database import db
from src.model.vehicle import Vehicle, OilStatus
import datetime

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
        vehicle = Vehicle(id=1, name="Test Car", color="Blue", expenses=1000.0, mileage=10000, note="Test Note")
        db.session.add(vehicle)
        db.session.commit()
        yield vehicle

def test_add_vehicle(app):
    with app.app_context():
        vehicle = Vehicle(id=2, name="New Car", color="Red", expenses=500.0, mileage=5000, note="New Note")
        vehicle.add_vehicle()
        retrieved_vehicle = Vehicle.query.get(2)
        assert retrieved_vehicle is not None
        assert retrieved_vehicle.name == "New Car"
        assert retrieved_vehicle.color == "Red"
        assert retrieved_vehicle.expenses == 500.0
        assert retrieved_vehicle.mileage == 5000
        assert retrieved_vehicle.note == "New Note"

def test_get_vehicles(app, init_vehicle):
    with app.app_context():
        vehicles = Vehicle.get_vehicles()
        assert len(vehicles) == 1
        assert vehicles[0].name == "Test Car"

def test_edit_vehicle(app, init_vehicle):
    with app.app_context():
        vehicle = Vehicle.query.get(1)
        vehicle.edit_vehicle(name="Updated Car", color="Green", expenses=2000.0, mileage=15000, note="Updated Note")
        updated_vehicle = Vehicle.query.get(1)
        assert updated_vehicle.name == "Updated Car"
        assert updated_vehicle.color == "Green"
        assert updated_vehicle.expenses == 2000.0
        assert updated_vehicle.mileage == 15000
        assert updated_vehicle.note == "Updated Note"

def test_delete_vehicle(app, init_vehicle):
    with app.app_context():
        vehicle = Vehicle.query.get(1)
        vehicle.delete_vehicle()
        deleted_vehicle = Vehicle.query.get(1)
        assert deleted_vehicle is None

def test_add_oil_status(app, init_vehicle):
    with app.app_context():
        oil_status = OilStatus(vehicle_id=1, date_of_change=datetime.datetime.now(), mileage_when_changed=10500, note="Oil change note")
        db.session.add(oil_status)
        db.session.commit()
        oil_status_records = OilStatus.query.filter_by(vehicle_id=1).all()
        assert len(oil_status_records) == 1
        assert oil_status_records[0].mileage_when_changed == 10500
        assert oil_status_records[0].note == "Oil change note"
