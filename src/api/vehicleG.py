import json
from random import randint

from flask import request
from flask_restx import Namespace, Resource, fields

from src.model.vehicle import Vehicle

# namespace for vehicle related operations
vehicle_api = Namespace('vehicle', description='Vehicle related operations')


# MODELS: make new ones as data changes

#Keep create_vehicle simple
create_vehicle_model = vehicle_api.model('Vehicle', {
    "name": fields.String(required=True, description='Give the vehicle a name'),
    "color": fields.String(required=True, description='The color of the vehicle'),
    "expenses": fields.Float(required=False, description='The total expenses of the vehicle'),
    "mileage": fields.Integer(required=True, description='The milage of the vehicle'),
    "note": fields.String(required=False, description='Additional notes about the vehicle'),
})

# model for retrieving vehicle details
get_vehicle_model = vehicle_api.model('Vehicle', {
    "id": fields.Integer(required=True, description='The vehicle id'),
    "name": fields.String(required=True, description='Give the vehicle a name'),
    "color": fields.String(required=True, description='The color of the vehicle'),
    "expenses": fields.Float(required=False, description='The total expenses of the vehicle'),
    "mileage": fields.Integer(required=True, description='The mileage of the vehicle'),
    "fuel_consumption": fields.Float(required=False, description='The fuel consumption of the vehicle'),
    "note": fields.String(required=False, description='Additional notes about the vehicle'),
})

# model for editing vehicle details
edit_vehicle_model = vehicle_api.model('EditVehicle', {
    "name": fields.String(required=False, description='Give the vehicle a name'),
    "color": fields.String(required=False, description='The color of the vehicle'),
    "expenses": fields.Float(required=False, description='The total expenses of the vehicle'),
    "mileage": fields.Integer(required=False, description='The mileage of the vehicle'),
    "fuel_consumption": fields.Float(required=False, description='The fuel consumption of the vehicle'),
    "note": fields.String(required=False, description='Additional notes about the vehicle'),
})


# API Routes
@vehicle_api.route('/')
class VehicleList(Resource):



    @vehicle_api.doc(create_vehicle_model, description='Add a vehicle to the database')
    @vehicle_api.expect(create_vehicle_model, validate=True)
    @vehicle_api.marshal_with(create_vehicle_model, envelope='vehicle')
    def post(self):

        # add a new vehicle

        id = Vehicle.give_me_id()  # Generate a unique ID for the new vehicle

        # create a new vehicle instance with the provided data
        new_vehicle = Vehicle(id=id,
                              name=vehicle_api.payload["name"],
                              color=vehicle_api.payload["color"],
                              expenses=vehicle_api.payload["expenses"],
                              mileage=vehicle_api.payload['mileage'],
                              # No need for fuel_consumption yet
                              note=vehicle_api.payload["note"])

        # add the vehicle to the database
        Vehicle.add_vehicle(new_vehicle)
        return new_vehicle, 201




    @vehicle_api.marshal_with(get_vehicle_model, envelope='vehicle')
    def get(self):

        # get all vehicles from the db

        vehicles = Vehicle.get_vehicles()
        vehicles_json = [v.dict_data() for v in vehicles]


        return vehicles_json, 200



    @vehicle_api.doc(description='Delete a vehicle from the database')
    @vehicle_api.response(204, 'Vehicle deleted successfully')
    @vehicle_api.response(404, 'Vehicle not found')
    @vehicle_api.param('id', 'ID of the vehicle to delete', type=int)
    def delete(self):

        # delete a vehicle

        try:
            vehicle_id = int(request.args.get('id'))
            vehicle = Vehicle.query.get(vehicle_id)
            if vehicle:
                Vehicle.delete_vehicle(vehicle)
                return 'Vehicle deleted', 204
            else:
                return {'error': 'Vehicle not found'}, 404
        except Exception as e:
            return {'error': 'Failed to delete vehicle', 'details': str(e)}, 500



    @vehicle_api.doc(edit_vehicle_model, description='Edit a vehicle in the database')
    @vehicle_api.expect(edit_vehicle_model, validate=True)
    @vehicle_api.response(200, 'Vehicle updated successfully')
    @vehicle_api.response(404, 'Vehicle not found')
    @vehicle_api.param('id', 'ID of the vehicle to edit', type=int, required=True)
    def put(self):

        # edit the vehicle in the db

        try:
            vehicle_id = int(request.args.get('id'))
            vehicle = Vehicle.query.get(vehicle_id)
            if vehicle:
                data = request.json
                vehicle.edit_vehicle(
                    name=data.get("name"),
                    color=data.get("color"),
                    expenses=data.get("expenses"),
                    mileage=data.get("mileage"),
                    fuel_consumption=data.get("fuel_consumption"),
                    note=data.get("note")
                )
                return {'message': 'Vehicle updated successfully'}, 200
            else:
                return {'error': 'Vehicle not found'}, 404
        except Exception as e:
            return {'error': 'Failed to update vehicle', 'details': str(e)}, 500




