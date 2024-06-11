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
