import pytest
from src.database import db
from src.model.vehicle import Vehicle

@pytest.fixture
def vehicle():
    return Vehicle(id=1, name="Test Car", color="Red", expenses=0.0, mileage=0, note="Test Note")

def test_vehicle_creation(vehicle):
    assert vehicle.name == "Test Car"
    assert vehicle.color == "Red"
    assert vehicle.expenses == 0.0
    assert vehicle.mileage == 0
    assert vehicle.note == "Test Note"
