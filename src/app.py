from flask import Flask, render_template, request, jsonify
from flask_restx import Api
import json
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
        return render_template("vehicles.html") # works (idk why underlined)

    @app.route('/add')
    def index2():
        return render_template("create_vehicle.html")

    @app.route('/save-vehicle', methods=['POST'])
    def save_vehicle():
        vehicle_data = request.json
        try:

            file_path = 'src/static/create_vehicle.json' # for some reason the scope is so far out

            with open(file_path, 'w') as file:
                json.dump(vehicle_data, file, indent=4)
            return jsonify({'message': 'Vehicle data saved successfully'}), 200
        except Exception as e:
            print("Error:", str(e))  # Print the error message to the console
            return jsonify({'error': 'Failed to save vehicle data'}), 500

    return app
