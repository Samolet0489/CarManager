from typing import List, Optional
import json
from src.database import db
from flask_restx import Namespace, fields
from random import randint
from .refuel_history import RefuelHistory
from .important_dates import ImportantDates
from flask import jsonify

# namespace for vehicle-related operations
frontendVehicle = Namespace('vehicle', description='Vehicle related operations')

# adding a model so that I can send the data to the
create_vehicle_model = frontendVehicle.model('Vehicle', {
    "name": fields.String(required=True, description='Give the vehicle a name'),
    "color": fields.String(required=True, description='The color of the vehicle'),
    "expenses": fields.Float(required=False, description='The total expenses of the vehicle'),
    "mileage": fields.Integer(required=True, description='The milage of the vehicle'),
    "fuel_consumption": fields.Float(required=False, default=0,description='The fuel consumption of the vehicle'),
    "note": fields.String(required=False, description='Additional notes about the vehicle'),
})

class Vehicle(db.Model):

    __tablename__ = 'vehicle'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    color = db.Column(db.String(30), nullable=False)
    expenses = db.Column(db.Float, nullable=False)
    mileage = db.Column(db.Float, nullable=False)
    fuel_consumption = db.Column(db.Float, nullable=False)
    note = db.Column(db.String(500), nullable=True)

    # relationships
    refuel_history = db.relationship('RefuelHistory', back_populates='vehicle')
    important_dates = db.relationship('ImportantDates', back_populates='vehicle', uselist=False)
    oil_statuses = db.relationship('OilStatus', back_populates='vehicle')

    def __init__(self, id: int, name: str, color: str, expenses: float, mileage: float, note: str):
        self.id = id
        self.name = name  # here people can call their vehicle however they want
        self.color = color  # people can set the exact color of the vehicle (in case of an accident the mechanic knows the paint)
        self.expenses = expenses  # total expenses (just adding up all expenses ever accumulated)
        self.mileage = mileage
        self.fuel_consumption = 0  # default fuel consumption
        self.note = note  # additional notes

    # convert vehicle data to a dictionary
    def dict_data(self):
        important_dates_data = ImportantDates.query.filter_by(vehicle_id=self.id).first()
        oil_statuses_data = OilStatus.query.filter_by(vehicle_id=self.id).all()
        return {
            'id': self.id,
            'name': self.name,
            'color': self.color,
            'expenses': self.expenses,
            'mileage': self.mileage,
            'fuel_consumption': self.fuel_consumption,
            'note': self.note,
            'important_dates': {
                'car_tax': important_dates_data.car_tax.strftime('%Y-%m-%d') if important_dates_data and important_dates_data.car_tax else None,
                'annual_insurance': important_dates_data.annual_insurance.strftime('%Y-%m-%d') if important_dates_data and important_dates_data.annual_insurance else None,
                'technical_review': important_dates_data.technical_review.strftime('%Y-%m-%d') if important_dates_data and important_dates_data.technical_review else None,
                'vignette': important_dates_data.vignette.strftime('%Y-%m-%d') if important_dates_data and important_dates_data.vignette else None,
                'additional_insurance': important_dates_data.additional_insurance.strftime('%Y-%m-%d') if important_dates_data and important_dates_data.additional_insurance else None
            },
            'oil_statuses': [
                {
                    'date_of_change': oil_status.date_of_change.strftime('%Y-%m-%d'),
                    'mileage_when_changed': oil_status.mileage_when_changed,
                    'note': oil_status.note
                }
                for oil_status in oil_statuses_data
            ]
        }

    # generate a unique ID for a new vehicle
    @staticmethod
    def give_me_id():
        try:
            ids = [vehicle.id for vehicle in Vehicle.query.all()]  # we retrieve the IDs
            new_id = randint(0, 99999999999)
            while new_id in ids:
                new_id = randint(0, 99999999999)
            return new_id
        except Exception as e:
            print("Error:", e)
            return 0

    # add a vehicle to the database
    def add_vehicle(self):
        db.session.add(self)
        db.session.commit()

    # get all vehicles
    @staticmethod
    def get_vehicles():
        data = Vehicle.query.all()
        vehicles_json = [v.dict_data() for v in data]
        with open("src/static/generated/get_vehicles.json", "w") as f:
            f.write(json.dumps(vehicles_json, indent=4))
        return data

    # update fuel consumption
    def _fuel_consumption(self, fuel: float, mileage: float, current_mileage: float):
        self.fuel_consumption = (fuel / (current_mileage - mileage)) * 100 if current_mileage != mileage else 0
        self.mileage = current_mileage

    # add vehicle data to the database from JSON
    def add_vehicle_to_db(self):
        with open("./src/static/generated/create_vehicle.json", "r") as f:
            data = f.read()
            data_dict = json.loads(data)

        id = Vehicle.give_me_id()

        new_vehicle = Vehicle(id=id,
                              name=data_dict["name"],
                              color=data_dict["color"],
                              expenses=data_dict["expenses"],
                              mileage=data_dict['mileage'],
                              note=data_dict["note"])

        db.session.add(new_vehicle)
        db.session.commit()

    # Delete a vehicle and its ASSOCIATED records!!!
    def delete_vehicle(self):
        # delete all associated refuel history records
        RefuelHistory.query.filter_by(vehicle_id=self.id).delete()
        # delete all associated important dates records
        ImportantDates.query.filter_by(vehicle_id=self.id).delete()
        # delete all associated oil status records
        OilStatus.query.filter_by(vehicle_id=self.id).delete()
        db.session.delete(self)
        db.session.commit()

    # edit vehicle details
    def edit_vehicle(self, name: Optional[str] = None, color: Optional[str] = None, expenses: Optional[float] = None, mileage: Optional[float] = None, fuel_consumption: Optional[float] = None, note: Optional[str] = None):
        if name is not None:
            self.name = name
        if color is not None:
            self.color = color
        if expenses is not None:
            self.expenses = expenses
        if mileage is not None:
            self.mileage = mileage
        if fuel_consumption is not None:
            self.fuel_consumption = fuel_consumption
        if note is not None:
            self.note = note
        db.session.commit()
        print("Vehicle updated successfully")

    # does the car need to know about the mechanic? probably not
    def add_mechanic(self):
        pass  # add a way to set the mechanic to the vehicle.

# FUEL operations:
    def refuel(self, amount: float, current_mileage: float, price_per_liter: float, total_price: float):
        # Check if the new mileage is less than the previous mileage
        if current_mileage < self.mileage:
            raise ValueError('Current mileage cannot be less than the previous mileage.')

        # Calculate fuel consumption
        liters_used = amount
        if self.mileage != current_mileage:
            fuel_consumption = (liters_used / (current_mileage - self.mileage)) * 100
            fuel_consumption = round(fuel_consumption, 1)
        else:
            fuel_consumption = 0

        # Update vehicle's fuel consumption and mileage
        self.fuel_consumption = fuel_consumption
        self.mileage = current_mileage

        new_refuel = RefuelHistory(
            vehicle_id=self.id,
            amount=liters_used,
            mileage=current_mileage,
            price_per_liter=price_per_liter,
            total_price=total_price
        )

        db.session.add(new_refuel)
        db.session.commit()

    # get refuel history for the vehicle
    def get_refuel_history(self):
        return RefuelHistory.query.filter_by(vehicle_id=self.id).all()


    # this might be quite important or completely useless todo think about this
    # def set_owner(self):
    #     pass  # the car does not need to know about its owner



class OilStatus(db.Model):
    __tablename__ = 'oil_status'
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)
    date_of_change = db.Column(db.Date, nullable=False)
    mileage_when_changed = db.Column(db.Integer, nullable=False)
    note = db.Column(db.String(500), nullable=True)

    vehicle = db.relationship('Vehicle', back_populates='oil_statuses')

    def __init__(self, vehicle_id, date_of_change, mileage_when_changed, note=None):
        self.vehicle_id = vehicle_id
        self.date_of_change = date_of_change
        self.mileage_when_changed = mileage_when_changed
        self.note = note


