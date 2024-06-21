import pytest
from src.app import create_app
from src.database import db
from src.model.important_dates import ImportantDates

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_set_important_dates(client, app):
    with app.app_context():
        dates = ImportantDates(
            car_tax="2024-06-18",
            annual_insurance="2024-12-31",
            technical_review="2024-06-01",
            vignette="2024-11-11",
            additional_insurance="2024-09-09"
        )
        db.session.add(dates)
        db.session.commit()

        fetched_dates = ImportantDates.query.first()
        assert fetched_dates is not None
        assert fetched_dates.car_tax == "2024-06-18"
        assert fetched_dates.annual_insurance == "2024-12-31"
        assert fetched_dates.technical_review == "2024-06-01"
        assert fetched_dates.vignette == "2024-11-11"
        assert fetched_dates.additional_insurance == "2024-09-09"
