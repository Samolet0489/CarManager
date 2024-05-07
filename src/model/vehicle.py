from typing import List, Optional
import json
from src.database import db
from flask_restx import Namespace,fields
from random import randint



frontendVehicle = Namespace('vehicle', description='Vehicle related operations')
# adding a model so that I can send the data to the
create_vehicle_model = frontendVehicle.model('Vehicle', {
    "name": fields.String(required=True, description='Give the vehicle a name'),
    "color": fields.String(required=True, description='The color of the vehicle'),
    "expenses": fields.Float(required=False, description='The total expenses of the vehicle'),
    "mileage": fields.Integer(required=True, description='The milage of the vehicle'),
    "fuel_consumption": fields.Float(required=False, description='The fuel consumption of the vehicle'), # rn not in use
    "note": fields.String(required=False, description='Additional notes about the vehicle'),
})


class Vehicle(db.Model):

    __tablename__ = 'garage'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    color= db.Column(db.String(30), nullable=False)
    expenses = db.Column(db.Float, nullable=False)
    mileage = db.Column(db.Float, nullable=False)
    fuel_consumption = db.Column(db.Float, nullable=False)
    note = db.Column(db.String(500), nullable=True)

    # def repr(self):  # This makes it into a string representation
    #     return f'Vehicle {self.make} {self.model}'


    #todo make sure that the model fits this
    def __init__(self, id:int,name:str, color:str, expenses:float, mileage:float, note:str):
        self.id = id
        self.name = name # here people can call their vehicle however they want
        self.color = color  # people can set the exact color of the vehicle (in case of an accident the mechanic knows the paint)
        self.expenses = expenses # total expenses (just adding up all expenses ever accumulated)
        self.mileage = mileage
        self.fuel_consumption = 0 # TODO: now just needs to be added to the "fill up" method in vehicleG
        self.note = note # people can write a note with additional information about the car
        # feel free to add other info

    def dict_data(self):
        return {
            'id': self.id,
            'name': self.name,
            'color': self.color,
            'expenses': self.expenses,
            'mileage': self.mileage,
            'fuel_consumption': self.fuel_consumption,
            'note': self.note
        }

    @staticmethod
    def give_me_id():
        try:
            ids = [vehicle.id for vehicle in Vehicle.query.all()] # we retrieve the IDs
            # print(ids)
            # print(type(ids[0]))
            id = randint(0,99999999999)
            while id in ids:
                id = randint(0, 99999999999)
            return ids
        except Exception as e:
            print("Error:", e)
            return 0

    def add_vehicle(self):
        db.session.add(self)
        db.session.commit()


    @staticmethod
    def get_vehicles():
        data = Vehicle.query.all()

        vehicles_json = [v.dict_data() for v in data]

        with open("src/static/get_vehicles.json", "w") as f:
            f.write(json.dumps(vehicles_json,indent=4))

        return data


    # make a refuel method that will call this funtion
    def _fuel_consumption(self, fuel:float, mileage:float, current_mileage:float):
        self.fuel_consumption = (current_mileage - mileage) / fuel # calculate the fuel consumption
        self.mileage = current_mileage # set the new mileage of the car

    def add_vehicle_to_db(self):
        with open("./src/static/create_vehicle.json", "r") as f:
            data = f.read()
            data_dict = json.loads(data)
            print(data_dict)
            print(type(data_dict))

        # temp solution for creating a  bad ID:
        from random import randint
        id = Vehicle.give_me_id() #make THE ID SYSTEM!!!!!!

        new_vehicle = Vehicle(id=id,
                              name=data_dict["name"],
                              color=data_dict["color"],
                              expenses=data_dict["expenses"],
                              mileage=data_dict['mileage'],
                              note=data_dict["note"])

        # this works for now
        db.session.add(new_vehicle)
        db.session.commit()
        print("Vehicle added successfully")

    #todo add the remove button Mght have to do the inner info first
    def remove_vehicle(self):
        pass




