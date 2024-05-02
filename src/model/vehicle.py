from typing import List, Optional

from src.database import db


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


    def add_vehicle(self):
        db.session.add(self)
        db.session.commit()


    @staticmethod
    def get_vehicles():
        return Vehicle.query.all() # why doesnt this return the fuel consumption


    # make a refuel method that will call this funtion
    def _fuel_consumption(self, fuel:float, mileage:float, current_mileage:float):
        self.fuel_consumption = (current_mileage - mileage) / fuel # calculate the fuel consumption
        self.mileage = current_mileage # set the new mileage of the car






