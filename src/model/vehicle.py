from typing import List, Optional

from src.database import db


class Vehicle(db.Model):

    __tablename__ = 'garage'
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(30), nullable=False)
    model = db.Column(db.String(30), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    color= db.Column(db.String(30), nullable=False)
    price = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(30), nullable=False)
    mileage = db.Column(db.Float, nullable=False)

    # def repr(self):  # This makes it into a string reperesentation
    #     return f'Vehicle {self.make} {self.model}'


    #todo make sure that the model fits this
    def __init__(self, id:int,make:str, model:str, year:int, color:str, price:float, type:str, mileage:float):
        self.id = id
        self.make = make
        self.model = model
        self.year = year
        self.color = color
        self.price = price
        self.type = type
        self.mileage = mileage
        # other info

    def dict_data(self):
        return {
            'id': self.id,
            'make': self.make,
            'model': self.model,
            'year': self.year,
            'color': self.color,
            'price': self.price,
            'type': self.type,
            'mileage': self.mileage
        }


    def add_vehicle(self):
        db.session.add(self)
        db.session.commit()


    @staticmethod
    def get_vehicles():
        return Vehicle.query.all()




