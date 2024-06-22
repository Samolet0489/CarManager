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

@pytest.fixture
def init_mechanic(app):
    with app.app_context():
        mechanic = Mechanic(id=1, name="Test Mechanic", address="123 Test Street", email="test@mechanic.com", phone="1234567890", hourly_rate=50.0, note="Test Note")
        db.session.add(mechanic)
        db.session.commit()
        yield mechanic

def test_add_mechanic(app):
    with app.app_context():
        mechanic = Mechanic(id=2, name="New Mechanic", address="456 New Street", email="new@mechanic.com", phone="0987654321", hourly_rate=75.0, note="New Note")
        mechanic.add_mechanic()
        retrieved_mechanic = Mechanic.query.get(2)
        assert retrieved_mechanic is not None
        assert retrieved_mechanic.name == "New Mechanic"
        assert retrieved_mechanic.address == "456 New Street"
        assert retrieved_mechanic.email == "new@mechanic.com"
        assert retrieved_mechanic.phone == "0987654321"
        assert retrieved_mechanic.hourly_rate == 75.0
        assert retrieved_mechanic.note == "New Note"

def test_get_mechanics(app, init_mechanic):
    with app.app_context():
        mechanics = Mechanic.get_mechanic()
        assert len(mechanics) == 1
        assert mechanics[0].name == "Test Mechanic"

def test_delete_mechanic(app, init_mechanic):
    with app.app_context():
        mechanic = Mechanic.query.get(1)
        mechanic.delete_mechanic()
        deleted_mechanic = Mechanic.query.get(1)
        assert deleted_mechanic is None

def test_get_mechanic_id(app, init_mechanic):
    with app.app_context():
        mechanic = Mechanic.query.get(1)
        retrieved_mechanic = mechanic.get_mechanic_id(1)
        assert retrieved_mechanic is not None
        assert retrieved_mechanic.name == "Test Mechanic"
        assert retrieved_mechanic.address == "123 Test Street"
        assert retrieved_mechanic.email == "test@mechanic.com"
        assert retrieved_mechanic.phone == "1234567890"
        assert retrieved_mechanic.hourly_rate == 50.0
        assert retrieved_mechanic.note == "Test Note"

def test_give_me_id(app):
    with app.app_context():
        mechanic1 = Mechanic(id=1, name="Mechanic One", address="123 One Street", email="one@mechanic.com", phone="1234567890", hourly_rate=50.0, note="Note One")
        mechanic2 = Mechanic(id=2, name="Mechanic Two", address="456 Two Street", email="two@mechanic.com", phone="0987654321", hourly_rate=75.0, note="Note Two")
        db.session.add(mechanic1)
        db.session.add(mechanic2)
        db.session.commit()

        new_id = Mechanic.give_me_id()
        assert new_id not in [mechanic1.id, mechanic2.id]
        assert isinstance(new_id, int)

def test_dict_data(app, init_mechanic):
    with app.app_context():
        mechanic = Mechanic.query.get(1)
        data = mechanic.dict_data()
        assert data['id'] == 1
        assert data['name'] == "Test Mechanic"
        assert data['address'] == "123 Test Street"
        assert data['email'] == "test@mechanic.com"
        assert data['phone'] == "1234567890"
        assert data['hourly_rate'] == 50.0
        assert data['note'] == "Test Note"
