from datetime import datetime
from src.database import db

class RefuelHistory(db.Model):
    __tablename__ = 'refuel_history'
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    mileage = db.Column(db.Float, nullable=False)
    price_per_liter = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    vehicle = db.relationship('Vehicle', back_populates='refuel_history')

    def __init__(self, vehicle_id, amount, mileage, price_per_liter, total_price):
        self.vehicle_id = vehicle_id
        self.amount = amount
        self.mileage = mileage
        self.price_per_liter = price_per_liter
        self.total_price = total_price

    @classmethod
    def get_fuel_mileage(cls, vehicle_id):
        # getting all the refuel records for a vehicles (ordered by millage - decreasing)
        refuels = cls.query.filter_by(vehicle_id=vehicle_id).order_by(cls.mileage.desc()).all()
        mileage_data = []

        # calculating the fuel consumption
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
