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

def test_get_mechanics(client):
    response = client.get('/mechanics')
    assert response.status_code == 200
    assert b"Mechanics" in response.data

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