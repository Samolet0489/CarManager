from flask import Flask
from flask_restx import Api

from src.database import db
from .api.vehicleG import vehicle_api # a problem with this import

#import the NS models here (NS might stand fir newspaper so rename?)


def create_app():
    app = Flask(__name__)

    # configure the database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vehicles.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()

    api = Api(app) #  title= you can add a name

    # you have to add the namespace so flask will see the module
    api.add_namespace(vehicle_api)


    return app

if __name__ == '__main__':
    create_app().run(debug=False, port=5000) # see if you want to change the port