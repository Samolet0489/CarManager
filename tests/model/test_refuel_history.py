import pytest
from src.app import create_app
from src.database import db
from src.model.vehicle import Vehicle
from src.model.refuel_history import RefuelHistory

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

def test_refuel(app, init_vehicle):
    with app.app_context():
        vehicle = Vehicle.query.get(1)
        vehicle.refuel(amount=50, current_mileage=10500, price_per_liter=1.5, total_price=75)
        assert vehicle.fuel_consumption == pytest.approx(10.0)
        assert vehicle.mileage == 10500
        refuel_records = RefuelHistory.query.filter_by(vehicle_id=1).all()
        assert len(refuel_records) == 1
        assert refuel_records[0].amount == 50
        assert refuel_records[0].mileage == 10500
        assert refuel_records[0].price_per_liter == 1.5
        assert refuel_records[0].total_price == 75

def test_refuel_invalid_mileage(app, init_vehicle):
    with app.app_context():
        vehicle = Vehicle.query.get(1)
        with pytest.raises(ValueError):
            vehicle.refuel(amount=50, current_mileage=9500, price_per_liter=1.5, total_price=75)

def test_get_refuel_history(app, init_vehicle):
    with app.app_context():
        vehicle = Vehicle.query.get(1)
        vehicle.refuel(amount=50, current_mileage=10500, price_per_liter=1.5, total_price=75)
        refuel_history = vehicle.get_refuel_history()
        assert len(refuel_history) == 1
        assert refuel_history[0].amount == 50
        assert refuel_history[0].mileage == 10500
        assert refuel_history[0].price_per_liter == 1.5
        assert refuel_history[0].total_price == 75
