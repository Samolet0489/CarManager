import pytest
from datetime import datetime
from src.app import create_app
from src.database import db
from src.model.important_dates import ImportantDates
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

@pytest.fixture
def init_vehicle(app):
    with app.app_context():
        vehicle = Vehicle(id=1, name="Test Car", color="Red", expenses=1000.0, mileage=10000, note="Test Note")
        db.session.add(vehicle)
        db.session.commit()
        yield vehicle

def test_add_important_dates(app, init_vehicle):
    with app.app_context():
        dates = ImportantDates(
            vehicle_id=1,
            car_tax=datetime(2023, 1, 1),
            annual_insurance=datetime(2023, 2, 1),
            technical_review=datetime(2023, 3, 1),
            vignette=datetime(2023, 4, 1),
            additional_insurance=datetime(2023, 5, 1)
        )
        db.session.add(dates)
        db.session.commit()
        retrieved_dates = ImportantDates.query.filter_by(vehicle_id=1).first()
        assert retrieved_dates is not None
        assert retrieved_dates.car_tax == datetime(2023, 1, 1).date()
        assert retrieved_dates.annual_insurance == datetime(2023, 2, 1).date()
        assert retrieved_dates.technical_review == datetime(2023, 3, 1).date()
        assert retrieved_dates.vignette == datetime(2023, 4, 1).date()
        assert retrieved_dates.additional_insurance == datetime(2023, 5, 1).date()

def test_get_important_dates(app, init_vehicle):
    with app.app_context():
        dates = ImportantDates(
            vehicle_id=1,
            car_tax=datetime(2023, 1, 1),
            annual_insurance=datetime(2023, 2, 1),
            technical_review=datetime(2023, 3, 1),
            vignette=datetime(2023, 4, 1),
            additional_insurance=datetime(2023, 5, 1)
        )
        db.session.add(dates)
        db.session.commit()

        retrieved_dates = ImportantDates.get_important_dates(1)
        assert retrieved_dates is not None
        assert retrieved_dates.car_tax == datetime(2023, 1, 1).date()
        assert retrieved_dates.annual_insurance == datetime(2023, 2, 1).date()
        assert retrieved_dates.technical_review == datetime(2023, 3, 1).date()
        assert retrieved_dates.vignette == datetime(2023, 4, 1).date()
        assert retrieved_dates.additional_insurance == datetime(2023, 5, 1).date()

def test_update_important_dates(app, init_vehicle):
    with app.app_context():
        dates = ImportantDates(
            vehicle_id=1,
            car_tax=datetime(2023, 1, 1),
            annual_insurance=datetime(2023, 2, 1),
            technical_review=datetime(2023, 3, 1),
            vignette=datetime(2023, 4, 1),
            additional_insurance=datetime(2023, 5, 1)
        )
        db.session.add(dates)
        db.session.commit()

        updated_dates = ImportantDates.update_important_dates(
            vehicle_id=1,
            car_tax='2024-01-01',
            annual_insurance='2024-02-01',
            technical_review='2024-03-01',
            vignette='2024-04-01',
            additional_insurance='2024-05-01'
        )

        assert updated_dates.car_tax == datetime(2024, 1, 1).date()
        assert updated_dates.annual_insurance == datetime(2024, 2, 1).date()
        assert updated_dates.technical_review == datetime(2024, 3, 1).date()
        assert updated_dates.vignette == datetime(2024, 4, 1).date()
        assert updated_dates.additional_insurance == datetime(2024, 5, 1).date()
