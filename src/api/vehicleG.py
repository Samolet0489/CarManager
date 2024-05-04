import json
from random import randint

from flask_restx import Namespace, Resource, fields

from src.model.vehicle import Vehicle

vehicle_api = Namespace('vehicle', description='Vehicle related operations')


# Models: make new ones as data changes
#Keep create_vehicle simple
create_vehicle_model = vehicle_api.model('Vehicle', {
    "name": fields.String(required=True, description='Give the vehicle a name'),
    "color": fields.String(required=True, description='The color of the vehicle'),
    "expenses": fields.Float(required=False, description='The total expenses of the vehicle'),
    "mileage": fields.Integer(required=True, description='The milage of the vehicle'),
    "note": fields.String(required=False, description='Additional notes about the vehicle'),
})


get_vehicle_model = vehicle_api.model('Vehicle', {
    "name": fields.String(required=True, description='Give the vehicle a name'),
    "color": fields.String(required=True, description='The color of the vehicle'),
    "expenses": fields.Float(required=False, description='The total expenses of the vehicle'),
    "mileage": fields.Integer(required=True, description='The milage of the vehicle'),
    "fuel_consumption": fields.Float(required=False, description='The fuel consumption of the vehicle'),
    "note": fields.String(required=False, description='Additional notes about the vehicle'),
})



@vehicle_api.route('/')
class VehicleList(Resource):

    #working on making the basic methods for CRUD
    @vehicle_api.doc(create_vehicle_model, description='Add a vehicle to the database')
    @vehicle_api.expect(create_vehicle_model, validate=True)
    @vehicle_api.marshal_with(create_vehicle_model, envelope='vehicle')
    def post(self):
        id = randint(0,9999999999) #todo check for the id not to repeat

        # eventually this should get this data from the temp files
        new_vehicle = Vehicle(id=id,
                              name=vehicle_api.payload["name"],
                              color=vehicle_api.payload["color"],
                              expenses=vehicle_api.payload["expenses"],
                              mileage=vehicle_api.payload['mileage'],
                              # No need for fuel_consumption yet
                              note=vehicle_api.payload["note"])

        Vehicle.add_vehicle(new_vehicle)
        return new_vehicle, 201

    @vehicle_api.marshal_with(get_vehicle_model, envelope='vehicle')
    def get(self): # shows all vehicles

        vehicles = Vehicle.get_vehicles()
        vehicles_json = [v.dict_data() for v in vehicles]

        with open("src/temp_files/get_vehicles.json", "w") as f:
            f.write(json.dumps(vehicles_json,indent=4))

        return vehicles_json





    # writing the logic here will require some code in the garage
    # look into writing some code there first
    # maybe do a pytest before you get going on the project
    # please do pytests
