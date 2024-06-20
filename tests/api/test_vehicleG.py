import pytest
from src.model.vehicle import Vehicle
from src.app import create_app, db

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

def test_get_vehicles(client):
    response = client.get('/vehicles')
    assert response.status_code == 200
    assert b"Add a Vehicle" in response.data

def test_createVehicle(app):
    with app.app_context():
        new_vehicle = Vehicle(
            id=Vehicle.give_me_id(),
            name="Honda FMX650 2005",
            color="black",
            expenses=5000,
            mileage=43000,
            note="This is my motorcycle :D"
        )
        new_vehicle.add_vehicle()
        vehicle = Vehicle.query.get(new_vehicle.id)
        assert vehicle is not None
        assert vehicle.name == "Honda FMX650 2005"

def test_getVehicles(app):
    with app.app_context():
        vehicles = Vehicle.get_vehicles()
        assert vehicles is not None
