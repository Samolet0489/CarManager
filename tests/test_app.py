import pytest
from flask import url_for
from src.app import create_app
from src.database import db
from src.model.vehicle import Vehicle, OilStatus
from src.model.important_dates import ImportantDates
from src.model.mechanic import Mechanic
from src.model.refuel_history import RefuelHistory
import datetime

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

def test_index(client, app):
    with app.app_context():
        vehicle = Vehicle(id=1, name="Test Car", color="Red", expenses=1000.0, mileage=10000, note="Test Note")
        db.session.add(vehicle)
        db.session.commit()
    response = client.get('/vehicles')
    assert response.status_code == 200

def test_vehicle_info(client, app):
    with app.app_context():
        vehicle = Vehicle(id=1, name="Test Car", color="Red", expenses=1000.0, mileage=10000, note="Test Note")
        db.session.add(vehicle)
        db.session.commit()
    response = client.get('/vehicle/1/info')
    assert response.status_code == 200

def test_index2(client):
    response = client.get('/add')
    assert response.status_code == 200

def test_save_vehicle(client):
    vehicle_data = {
        'name': 'Test Car',
        'color': 'Blue',
        'expenses': 1000.0,
        'mileage': 10000,
        'note': 'Test Note'
    }
    response = client.post('/save-vehicle', json=vehicle_data)
    assert response.status_code == 200

def test_delete_vehicle(client, app):
    with app.app_context():
        vehicle = Vehicle(id=1, name="Test Car", color="Red", expenses=1000.0, mileage=10000, note="Test Note")
        db.session.add(vehicle)
        db.session.commit()
    response = client.post('/delete_vehicle', json={'id': 1})
    assert response.status_code == 200

def test_edit_vehicle(client, app):
    with app.app_context():
        vehicle = Vehicle(id=1, name="Test Car", color="Red", expenses=1000.0, mileage=10000, note="Test Note")
        db.session.add(vehicle)
        db.session.commit()
    response = client.post('/edit_vehicle/1', data={
        'name': 'Updated Car',
        'color': 'Blue',
        'expenses': 1500.0,
        'mileage': 15000,
        'note': 'Updated Note'
    })
    assert response.status_code == 302

def test_fuel_vehicle(client, app):
    with app.app_context():
        vehicle = Vehicle(id=1, name="Test Car", color="Red", expenses=1000.0, mileage=10000, note="Test Note")
        db.session.add(vehicle)
        db.session.commit()
    response = client.post('/fuel_vehicle/1', data={
        'amount': 50,
        'mileage': 10500,
        'price_per_liter': 1.5,
        'total_price': 75
    })
    assert response.status_code == 302

def test_update_refuel(client, app):
    with app.app_context():
        vehicle = Vehicle(id=1, name="Test Car", color="Red", expenses=1000.0, mileage=10000, note="Test Note")
        db.session.add(vehicle)
        db.session.commit()
        refuel = RefuelHistory(vehicle_id=1, amount=50, mileage=10500, price_per_liter=1.5, total_price=75)
        db.session.add(refuel)
        db.session.commit()
        refuel_id = refuel.id

    response = client.post(f'/update_refuel/{refuel_id}', data={
        'amount': 60,
        'mileage': 10600,
        'price_per_liter': 1.6,
        'total_price': 96
    })
    assert response.status_code == 302

    with app.app_context():
        updated_refuel = RefuelHistory.query.get(refuel_id)
        assert updated_refuel.amount == 60
        assert updated_refuel.mileage == 10600
        assert updated_refuel.price_per_liter == 1.6
        assert updated_refuel.total_price == 96



def test_delete_refuel(client, app):
    with app.app_context():
        vehicle = Vehicle(id=1, name="Test Car", color="Red", expenses=1000.0, mileage=10000, note="Test Note")
        db.session.add(vehicle)
        db.session.commit()
        refuel = RefuelHistory(vehicle_id=1, amount=50, mileage=10500, price_per_liter=1.5, total_price=75)
        db.session.add(refuel)
        db.session.commit()
        refuel_id = refuel.id

    response = client.post(f'/delete_refuel/{refuel_id}')
    assert response.status_code == 302

    with app.app_context():
        deleted_refuel = RefuelHistory.query.get(refuel_id)
        assert deleted_refuel is None



def test_important_dates_route(client, app):
    with app.app_context():
        vehicle = Vehicle(id=1, name="Test Car", color="Red", expenses=1000.0, mileage=10000, note="Test Note")
        db.session.add(vehicle)
        db.session.commit()
    response = client.get('/important_dates/1')
    assert response.status_code == 200

def test_mechanics(client, app):
    with app.app_context():
        mechanic = Mechanic(id=1, name="Test Mechanic", address="123 Test Street", email="test@mechanic.com", phone="1234567890", hourly_rate=50.0, note="Test Note")
        db.session.add(mechanic)
        db.session.commit()
    response = client.get('/mechanics')
    assert response.status_code == 200

def test_add_mechanic_form(client):
    response = client.get('/add_mechanic')
    assert response.status_code == 200

def test_save_mechanic(client):
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

def test_edit_mechanic(client, app):
    with app.app_context():
        mechanic = Mechanic(id=1, name="Test Mechanic", address="123 Test Street", email="test@mechanic.com", phone="1234567890", hourly_rate=50.0, note="Test Note")
        db.session.add(mechanic)
        db.session.commit()
    response = client.post('/edit_mechanic/1', json={
        'name': 'Updated Mechanic',
        'address': '456 Updated Street',
        'email': 'updated@mechanic.com',
        'phone': '0987654321',
        'hourly_rate': 75.0,
        'note': 'Updated Note'
    })
    assert response.status_code == 200

def test_delete_mechanic(client, app):
    with app.app_context():
        mechanic = Mechanic(id=1, name="Test Mechanic", address="123 Test Street", email="test@mechanic.com", phone="1234567890", hourly_rate=50.0, note="Test Note")
        db.session.add(mechanic)
        db.session.commit()
    response = client.post('/delete_mechanic/1')
    assert response.status_code == 200

def test_edit_oil_status(client, app):
    with app.app_context():
        vehicle = Vehicle(id=1, name="Test Car", color="Red", expenses=1000.0, mileage=10000, note="Test Note")
        db.session.add(vehicle)
        db.session.commit()
    response = client.post('/vehicle/1/oil', data={
        'date_of_change': '2023-06-01',
        'mileage_when_changed': 10500,
        'note': 'Oil change note'
    })
    assert response.status_code == 302

# def test_edit_specific_oil_status(client, app):
#     with app.app_context():
#         vehicle = Vehicle(id=1, name="Test Car", color="Red", expenses=1000.0, mileage=10000, note="Test Note")
#         db.session.add(vehicle)
#         db.session.commit()
#         oil_status = OilStatus(vehicle_id=1, date_of_change=datetime.datetime.now(), mileage_when_changed=10500, note="Oil change note")
#         db.session.add(oil_status)
#         db.session.commit()
#         oil_id = oil_status.id
#
#     response = client.post(f'/vehicle/1/edit_oil/{oil_id}', data={
#         'date_of_change': '2023-07-01',
#         'mileage_when_changed': 10600,
#         'note': 'Updated oil change note'
#     })
#     assert response.status_code == 302
#
#     with app.app_context():
#         updated_oil_status = OilStatus.query.get(oil_id)
#         assert updated_oil_status.date_of_change.date() == datetime.date(2023, 7, 1)  # Compare only the date part
#         assert updated_oil_status.mileage_when_changed == 10600
#         assert updated_oil_status.note == 'Updated oil change note'


