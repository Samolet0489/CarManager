import pytest
from src.app import create_app
from src.model.vehicle import Vehicle
from src.model.important_dates import ImportantDates
from src.database import db
from datetime import datetime

@pytest.fixture
def app():
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True

    with app.app_context():
        db.create_all()
        yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_set_important_dates(client, app):
    # Create vehicle first
    vehicle_data = {
        'name': 'Test Car',
        'color': 'Blue',
        'expenses': 1000.0,
        'mileage': 10000,
        'note': 'Test Note'
    }
    client.post('/save-vehicle', json=vehicle_data)

    # Set important dates
    with app.app_context():
        vehicle = Vehicle.query.filter_by(name='Test Car').first()
        important_dates_data = {
            'vehicle_id': vehicle.id,
            'car_tax': '2024-06-01',
            'annual_insurance': '2024-06-15',
            'technical_review': '2024-07-01',
            'vignette': '2024-07-15',
            'additional_insurance': '2024-08-01'
        }
        response = client.post(f'/important_dates/{vehicle.id}', data=important_dates_data)
        assert response.status_code == 302  # Assuming it redirects after setting dates

        # Ensure the dates are in the database
        dates = ImportantDates.query.filter_by(vehicle_id=vehicle.id).first()
        assert dates is not None
        assert dates.car_tax == datetime.strptime('2024-06-01', '%Y-%m-%d').date()
        assert dates.annual_insurance == datetime.strptime('2024-06-15', '%Y-%m-%d').date()
        assert dates.technical_review == datetime.strptime('2024-07-01', '%Y-%m-%d').date()
        assert dates.vignette == datetime.strptime('2024-07-15', '%Y-%m-%d').date()
        assert dates.additional_insurance == datetime.strptime('2024-08-01', '%Y-%m-%d').date()
