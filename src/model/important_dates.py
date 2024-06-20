from datetime import datetime
from src.database import db

class ImportantDates(db.Model):
    __tablename__ = 'important_dates'
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)
    car_tax = db.Column(db.Date, nullable=True)
    annual_insurance = db.Column(db.Date, nullable=True)
    technical_review = db.Column(db.Date, nullable=True)
    vignette = db.Column(db.Date, nullable=True)
    additional_insurance = db.Column(db.Date, nullable=True)

    vehicle = db.relationship('Vehicle', back_populates='important_dates')

    def __init__(self, vehicle_id, car_tax=None, annual_insurance=None, technical_review=None, vignette=None, additional_insurance=None):
        self.vehicle_id = vehicle_id
        self.car_tax = car_tax
        self.annual_insurance = annual_insurance
        self.technical_review = technical_review
        self.vignette = vignette
        self.additional_insurance = additional_insurance
