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

    @staticmethod
    def get_important_dates(vehicle_id):
        return ImportantDates.query.filter_by(vehicle_id=vehicle_id).first()

    @staticmethod
    def update_important_dates(vehicle_id, car_tax, annual_insurance, technical_review, vignette, additional_insurance):
        car_tax_date = datetime.strptime(car_tax, '%Y-%m-%d').date() if car_tax else None
        annual_insurance_date = datetime.strptime(annual_insurance, '%Y-%m-%d').date() if annual_insurance else None
        technical_review_date = datetime.strptime(technical_review, '%Y-%m-%d').date() if technical_review else None
        vignette_date = datetime.strptime(vignette, '%Y-%m-%d').date() if vignette else None
        additional_insurance_date = datetime.strptime(additional_insurance, '%Y-%m-%d').date() if additional_insurance else None

        dates = ImportantDates.query.filter_by(vehicle_id=vehicle_id).first()
        if not dates:
            dates = ImportantDates(vehicle_id=vehicle_id)

        dates.car_tax = car_tax_date
        dates.annual_insurance = annual_insurance_date
        dates.technical_review = technical_review_date
        dates.vignette = vignette_date
        dates.additional_insurance = additional_insurance_date

        db.session.add(dates)
        db.session.commit()

        return dates
