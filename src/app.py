from flask import Flask, render_template, send_from_directory
from flask_restx import Api

from src.database import db
from .api.vehicleG import vehicle_api

def create_app():
    app = Flask(__name__)

    # Configure the database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vehicles.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()

    api = Api(app)  # Initialize the Flask-RESTx API

    # Add the vehicle_api namespace to the API
    api.add_namespace(vehicle_api)

    # Define a route to render the vehicles.html template
    @app.route('/vehicles')
    def index():
        return render_template("vehicles.html")

    # Route to serve the JSON file
    @app.route('/static/<path:filename>')
    def get_json(filename):
        return send_from_directory('temp_files', filename)

    return app
