import pytest
from src.app import create_app
from src.model.vehicle import Vehicle
from src.model.important_dates import ImportantDates
from src.database import db
from datetime import datetime

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

def test_set_important_dates(client, app):
    with app.app_context():
        # Create and add a vehicle to the database
        vehicle = Vehicle(
            id=Vehicle.give_me_id(),
            name="Test Vehicle",
            color="Red",
            expenses=0.0,
            mileage=1000,
            note="Test Note"
        )
        db.session.add(vehicle)
        db.session.commit()

        # Create and add important dates for the vehicle
        dates = ImportantDates(
            vehicle_id=vehicle.id,
            car_tax=datetime.strptime("2024-06-18", '%Y-%m-%d').date(),
            annual_insurance=datetime.strptime("2024-12-31", '%Y-%m-%d').date(),
            technical_review=datetime.strptime("2024-06-01", '%Y-%m-%d').date(),
            vignette=datetime.strptime("2024-11-11", '%Y-%m-%d').date(),
            additional_insurance=datetime.strptime("2024-09-09", '%Y-%m-%d').date()
        )
        db.session.add(dates)
        db.session.commit()

        # Fetch the dates and verify
        fetched_dates = ImportantDates.query.filter_by(vehicle_id=vehicle.id).first()
        assert fetched_dates is not None
        assert fetched_dates.car_tax == datetime.strptime("2024-06-18", '%Y-%m-%d').date()
        assert fetched_dates.annual_insurance == datetime.strptime("2024-12-31", '%Y-%m-%d').date()
        assert fetched_dates.technical_review == datetime.strptime("2024-06-01", '%Y-%m-%d').date()
        assert fetched_dates.vignette == datetime.strptime("2024-11-11", '%Y-%m-%d').date()
        assert fetched_dates.additional_insurance == datetime.strptime("2024-09-09", '%Y-%m-%d').date()