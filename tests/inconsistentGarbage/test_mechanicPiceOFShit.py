import pytest
from src.app import create_app
from src.database import db
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

def test_update_mechanic(client, app):
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
        assert mechanic.address == '123 Test Street'
        assert mechanic.email == 'test@mechanic.com'
        assert mechanic.phone == '1234567890'
        assert mechanic.hourly_rate == 50.0
        assert mechanic.note == 'Test Note'

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
        db.session.commit()
        db.session.expire_all()
        mechanic = Mechanic.query.filter_by(name='Test Mechanic').first()
        assert mechanic is not None
        assert mechanic.address == '456 Updated Street'
        assert mechanic.email == 'updated@mechanic.com'
        assert mechanic.phone == '0987654321'
        assert mechanic.hourly_rate == 75.0
        assert mechanic.note == 'Updated Test Note'
