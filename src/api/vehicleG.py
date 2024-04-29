from random import randint

from flask import jsonify
from flask_restx import Namespace, Resource, fields

from src.database import db
from src.model.vehicle import Vehicle
from src.model.garage import Garage

vehicle_api = Namespace('vehicle', description='Vehicle related operations')


#TODO: this will have to modified (this is random things for testing)
vehicle_model = vehicle_api.model('Vehicle', {
    "make": fields.String(required=True, description='The make of the vehicle'),
    "model": fields.String(required=True, description='The model of the vehicle'),
    "year": fields.Integer(required=False, description='The year of the vehicle'),
    "color": fields.String(required=False, description='The color of the vehicle'),
    "price": fields.Float(required=False, description='The estimated price of the vehicle'),
    "type": fields.String(required=False, description='The type of vehicle'),
    "milage": fields.Integer(required=False, description='The milage of the vehicle'),
})



@vehicle_api.route('/')
class VehicleList(Resource):

    #working on making the basic methods for CRUD
    @vehicle_api.doc(vehicle_model, description='Add a vehicle to the database')
    @vehicle_api.expect(vehicle_model, validate=True)
    @vehicle_api.marshal_with(vehicle_model, envelope='vehicle')
    def post(self):
        id = randint(0,9999999999) #todo check for the id not to repeat

        new_vehicle = Vehicle(id=id,
                              make=vehicle_api.payload["make"],
                              model=vehicle_api.payload["model"],
                              year=vehicle_api.payload["year"],
                              color=vehicle_api.payload["color"],
                              price=vehicle_api.payload["price"],
                              type=vehicle_api.payload["type"],
                              mileage=vehicle_api.payload['milage'])
        db.session.add(new_vehicle)
        db.session.commit()
        return new_vehicle, 201

    @vehicle_api.marshal_with(vehicle_model, envelope='vehicle')
    def get(self): # shows all vehicles
        return Garage.query.all()





    # writing the logic here will require some code in the garage
    # look into writing some code there first
    # maybe do a pytest before you get going on the project
    # please do pytests
