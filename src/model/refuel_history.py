from datetime import datetime
from src.database import db

class RefuelHistory(db.Model):
    # table name in the database
    __tablename__ = 'refuel_history'
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)  # id of the vehicle
    amount = db.Column(db.Float, nullable=False)  # amount of fuel refueled
    mileage = db.Column(db.Float, nullable=False)  # mileage at the time of refueling
    price_per_liter = db.Column(db.Float, nullable=False)  # price per liter of fuel
    total_price = db.Column(db.Float, nullable=False)  # total price of the refuel
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  # timestamp of the refuel

    vehicle = db.relationship('Vehicle', back_populates='refuel_history')  # relationship to the Vehicle table

    def __init__(self, vehicle_id, amount, mileage, price_per_liter, total_price):
        self.vehicle_id = vehicle_id
        self.amount = amount
        self.mileage = mileage
        self.price_per_liter = price_per_liter
        self.total_price = total_price

    @classmethod
    def get_fuel_mileage(cls, vehicle_id):
        # get all refuel records for a vehicle, ordered by mileage (decreasing)
        refuels = cls.query.filter_by(vehicle_id=vehicle_id).order_by(cls.mileage.desc()).all()
        mileage_data = []

        # calculate fuel consumption
        for i in range(len(refuels) - 1):
            current_refuel = refuels[i]
            previous_refuel = refuels[i + 1]
            distance = current_refuel.mileage - previous_refuel.mileage
            if distance > 0:
                fuel_consumption = (current_refuel.amount / distance) * 100
                mileage_data.append((current_refuel, fuel_consumption))
            else:
                mileage_data.append((current_refuel, None))

        # the first refuel has no previous data
        if refuels:
            mileage_data.append((refuels[-1], None))

        return mileage_data

    @classmethod
    def update_refuel(cls, refuel_id, data):
        # update refuel record
        refuel = cls.query.get(refuel_id)
        if refuel:
            refuel.amount = float(data.get('amount'))
            refuel.mileage = float(data.get('mileage'))
            refuel.price_per_liter = float(data.get('price_per_liter'))
            refuel.total_price = float(data.get('total_price'))
            db.session.commit()
        return refuel

    @classmethod
    def delete_refuel(cls, refuel_id):
        # delete refuel record
        refuel = cls.query.get(refuel_id)
        if refuel:
            vehicle_id = refuel.vehicle_id
            db.session.delete(refuel)
            db.session.commit()
            return vehicle_id
        return None
