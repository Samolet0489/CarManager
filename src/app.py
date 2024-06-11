from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_restx import Api
import json
from src.database import db
from .api.vehicleG import vehicle_api
from .api.mechanicG import mechanic_api
from .model.refuel_history import RefuelHistory
from .model.vehicle import Vehicle

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
    api.add_namespace(mechanic_api)

    # Define a route to render the vehicles.html template
    @app.route('/vehicles')
    def index(): # load the default page for seeing our vehicles
        vehicles = Vehicle.get_vehicles()
        return render_template("vehicles.html", vehicles=vehicles) # Pass vehicles to the template

    @app.route('/<vehicle_name>/info')
    def vehicle_info(vehicle_name):
        vehicle = Vehicle.query.filter_by(name=vehicle_name).first()
        db.session.close()  # this might be a headache
        if vehicle:
            return render_template("vehicle_info.html", vehicle=vehicle)
        else:
            return jsonify({'error': 'Vehicle not found'}), 404

    @app.route('/add')
    def index2(): # load the page for adding vehicles
        return render_template("create_vehicle.html")

    @app.route('/save-vehicle', methods=['POST'])
    def save_vehicle():
        vehicle_data = request.json
        try:
            file_path = 'src/static/generated/create_vehicle.json' # for some reason the scope is so far out
            with open(file_path, 'w') as file:
                json.dump(vehicle_data, file, indent=4)
            Vehicle.add_vehicle_to_db(vehicle_data)
            return jsonify({'message': 'Vehicle data saved successfully'}), 200
        except Exception as e:
            print("Error:", str(e))  # Print the error message to the console
            return jsonify({'error': 'Failed to save vehicle data'}), 500

    @app.route('/delete_vehicle', methods=['POST'])  #now this works
    def delete_vehicle(): # a way to remove the vehicles
        try:
            vehicle_id = request.form.get("id")
            vehicle = Vehicle.query.get(vehicle_id)
            if vehicle:
                db.session.delete(vehicle) # remove it from the database
                # db.session.commit()
                # return jsonify({'message': 'Vehicle deleted successfully'}), 200
                return redirect("/vehicles",302)
            else:
                return jsonify({'error': 'Vehicle not found'}), 404
        except Exception as e:
            print("Error:", str(e))
            return jsonify({'error': 'Failed to delete vehicle'}), 500
        finally:
            db.session.commit()

    @app.route('/edit_vehicle/<int:vehicle_id>', methods=['GET', 'POST'])
    def edit_vehicle(vehicle_id):
        vehicle = Vehicle.query.get(vehicle_id)
        if request.method == 'POST':
            data = request.form
            vehicle.edit_vehicle(
                name=data.get("name"),
                color=data.get("color"),
                expenses=data.get("expenses"),
                mileage=data.get("mileage"),
                fuel_consumption=data.get("fuel_consumption"),
                note=data.get("note")
            )
            return redirect(url_for('vehicle_info', vehicle_name=vehicle.name))
        return render_template("edit_vehicle.html", vehicle=vehicle)

    @app.route('/fuel_vehicle/<int:vehicle_id>', methods=['GET', 'POST'])
    def fuel_vehicle(vehicle_id):
        vehicle = Vehicle.query.get(vehicle_id)
        if request.method == 'POST':
            try:
                amount = float(request.form.get('amount'))
                current_mileage = float(request.form.get('mileage'))
                price_per_liter = float(request.form.get('price_per_liter'))
                total_price = float(request.form.get('total_price'))
                vehicle.refuel(amount, current_mileage, price_per_liter, total_price)
                return redirect(url_for('fuel_vehicle', vehicle_id=vehicle.id))
            except ValueError as e:
                error = str(e)
                refuel_history = vehicle.get_refuel_history()
                return render_template("fuel.html", vehicle=vehicle, error=error, refuel_history=refuel_history)

        if vehicle:
            refuel_history = vehicle.get_refuel_history()
            return render_template("fuel.html", vehicle=vehicle, refuel_history=refuel_history)
        else:
            return jsonify({'error': 'Vehicle not found'}), 404

    return app
