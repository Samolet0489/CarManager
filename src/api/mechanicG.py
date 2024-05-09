from flask import request
from flask_restx import Namespace, Resource, fields

from src.model.mechanic import Mechanic

mechanic_api = Namespace("mechanic", description="Mechanic related operations")

create_mechanic_model = mechanic_api.model('CreateVehicle', {
    "name": fields.String(required=True, example="NAME"),
    "address": fields.String(required=True, example="address of the location"),
    "email": fields.String(required=True, example="EMAIL"),
    "phone": fields.String(required=True, example="555-555-5555"),
    "hourly_rate": fields.Float(required=True, example=60),
    "note": fields.String(required=True, example="note"),
})

get_mechanic_model = mechanic_api.model('CreateVehicle', {
    "id": fields.Integer(required=True, example=0),
    "name": fields.String(required=True, example="NAME"),
    "address": fields.String(required=True, example="address of the location"),
    "email": fields.String(required=True, example="EMAIL"),
    "phone": fields.String(required=True, example="555-555-5555"),
    "hourly_rate": fields.Float(required=True, example=60),
    "note": fields.String(required=True, example="note"),
})


@mechanic_api.route("/")
class MechanicList(Resource):

    @mechanic_api.doc(description="adding mechanics")
    @mechanic_api.expect(create_mechanic_model, validate=True)
    @mechanic_api.marshal_with(create_mechanic_model, envelope='mechanic')
    def post(self):
        id = Mechanic.give_me_id()

        new_mechanic = Mechanic(id=id,
                                name=mechanic_api.payload['name'],
                                address=mechanic_api.payload['address'],
                                email=mechanic_api.payload['email'],
                                phone=mechanic_api.payload['phone'],
                                hourly_rate=mechanic_api.payload['hourly_rate'],
                                note=mechanic_api.payload['note'])
        Mechanic.add_mechanic(new_mechanic)
        return new_mechanic, 201


    @mechanic_api.marshal_with(get_mechanic_model, description="getting all mechanics")
    def get(self):
        mechanics = Mechanic.get_mechanic()
        mechanic_json = [m.dict_data() for m in mechanics]
        return mechanic_json, 200

    #delete?!?!?
    @mechanic_api.doc(description="remove any mechanic mechanic")
    @mechanic_api.response(204, "Mechanic deleted")
    @mechanic_api.response(404, "Mechanic not found")
    @mechanic_api.param('id', "Id for the mechanic to remove")
    def delete(self):
        try:
            mechanic_id = int(request.args.get("id"))
            mechanic = Mechanic.query.get(mechanic_id)
            if mechanic:
                Mechanic.delete_mechanic(mechanic)
                return "Mechanic deleted", 204
            else:
                return "Mechanic not found", 404
        except Exception as e:
            return {"error": "Failed to delete mechanic", "details": str(e)}, 500

