from src.model.vehicle import Vehicle



#TODO: fix the tests or make them better (idk if they are broken or if the code is )

def test_createVehicle(): # the fixture vehicle is not good here you might have to look it up


    '''
    {
      "name": "Honda FMX650 2005",
      "color": "black",
      "expenses": 5000,
      "mileage": 43000,
      "fuel_consumption": 5.4,
      "note": "This is my motorcycle :D"
    }
    '''


    new_vehicle = Vehicle(
        id = 300,
        name="Honda FMX650 2005",
        color="black",
        expenses=5000,
        mileage=43000,
        note="This is my motorcycle :D"
    )

    Vehicle.add_vehicle(new_vehicle)

    print(new_vehicle.name)

    assert new_vehicle.name == "Honda FMX650 2005"
    # created the object but didnt actually work!?!?!?

def test_getVehicles(): # also not a good test fix me
    vehicles = Vehicle.get_vehicles()
    assert vehicles[0].name == "Honda FMX650 2005"
