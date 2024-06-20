import pytest
from src.model.mechanic import Mechanic

def test_get_mechanics(client):
    response = client.get('/mechanics')
    assert response.status_code == 200
    assert b"No mechanics found" in response.data  # Assuming this message when no mechanics are present

def test_create_mechanic(client, app):
    mechanic_data = {
        'name': 'Test Mechanic',
        'address': '123 Test Street',
        'email': 'test@mechanic.com',
        'phone': '1234567890',
        'hourly_rate': 50.0,
        'note': 'Test Note'
    }
    response = client.post('/save-mechanic', json=mechanic_data)
    assert response.status_code == 200

    # Ensure the mechanic is in the database
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
    # Create mechanic first
    mechanic_data = {
        'name': 'Test Mechanic',
        'address': '123 Test Street',
        'email': 'test@mechanic.com',
        'phone': '1234567890',
        'hourly_rate': 50.0,
        'note': 'Test Note'
    }
    client.post('/save-mechanic', json=mechanic_data)

    # Update mechanic
    updated_mechanic_data = {
        'name': 'Test Mechanic',
        'address': '456 Updated Street',
        'email': 'updated@mechanic.com',
        'phone': '0987654321',
        'hourly_rate': 75.0,
        'note': 'Updated Test Note'
    }
    response = client.post('/save-mechanic', json=updated_mechanic_data)
    assert response.status_code == 200

    # Ensure the mechanic is updated in the database
    with app.app_context():
        mechanic = Mechanic.query.filter_by(name='Test Mechanic').first()
        assert mechanic is not None
        assert mechanic.address == '456 Updated Street'
        assert mechanic.email == 'updated@mechanic.com'
        assert mechanic.phone == '0987654321'
        assert mechanic.hourly_rate == 75.0
        assert mechanic.note == 'Updated Test Note'

def test_delete_mechanic(client, app):
    # Create mechanic first
    mechanic_data = {
        'name': 'Test Mechanic',
        'address': '123 Test Street',
        'email': 'test@mechanic.com',
        'phone': '1234567890',
        'hourly_rate': 50.0,
        'note': 'Test Note'
    }
    client.post('/save-mechanic', json=mechanic_data)

    # Delete mechanic
    response = client.post('/delete-mechanic', json={'name': 'Test Mechanic'})
    assert response.status_code == 200

    # Ensure the mechanic is deleted from the database
    with app.app_context():
        mechanic = Mechanic.query.filter_by(name='Test Mechanic').first()
        assert mechanic is None
