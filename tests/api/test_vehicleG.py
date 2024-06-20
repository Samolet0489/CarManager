import pytest
from src.model.vehicle import Vehicle

def test_get_vehicles(client):
    response = client.get('/vehicles')
    assert response.status_code == 200
    assert b"No vehicles found" in response.data  # Assuming this message when no vehicles are present

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

    # Ensure the vehicle is in the database
    with app.app_context():
        vehicle = Vehicle.query.filter_by(name='Test Car').first()
        assert vehicle is not None
        assert vehicle.name == 'Test Car'
        assert vehicle.color == 'Blue'
        assert vehicle.expenses == 1000.0
        assert vehicle.mileage == 10000
        assert vehicle.note == 'Test Note'

def test_update_vehicle(client, app):
    # Create vehicle first
    vehicle_data = {
        'name': 'Test Car',
        'color': 'Blue',
        'expenses': 1000.0,
        'mileage': 10000,
        'note': 'Test Note'
    }
    client.post('/save-vehicle', json=vehicle_data)

    # Update vehicle
    updated_vehicle_data = {
        'name': 'Test Car',
        'color': 'Red',
        'expenses': 1500.0,
        'mileage': 15000,
        'note': 'Updated Test Note'
    }
    response = client.post('/save-vehicle', json=updated_vehicle_data)
    assert response.status_code == 200

    # Ensure the vehicle is updated in the database
    with app.app_context():
        vehicle = Vehicle.query.filter_by(name='Test Car').first()
        assert vehicle is not None
        assert vehicle.color == 'Red'
        assert vehicle.expenses == 1500.0
        assert vehicle.mileage == 15000
        assert vehicle.note == 'Updated Test Note'

def test_delete_vehicle(client, app):
    # Create vehicle first
    vehicle_data = {
        'name': 'Test Car',
        'color': 'Blue',
        'expenses': 1000.0,
        'mileage': 10000,
        'note': 'Test Note'
    }
    client.post('/save-vehicle', json=vehicle_data)

    # Delete vehicle
    response = client.post('/delete_vehicle', json={'name': 'Test Car'})
    assert response.status_code == 200

    # Ensure the vehicle is deleted from the database
    with app.app_context():
        vehicle = Vehicle.query.filter_by(name='Test Car').first()
        assert vehicle is None
