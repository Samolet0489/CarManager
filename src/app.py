from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_restx import Api
from datetime import datetime
import json
from src.database import db
from .api.vehicleG import vehicle_api
from .api.mechanicG import mechanic_api
from .model.refuel_history import RefuelHistory
from .model.vehicle import Vehicle
from .model.important_dates import ImportantDates
from .model.mechanic import Mechanic

def create_app():
    app = Flask(__name__)

    #Configure the database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vehicles.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()

    api = Api(app) # initialize the Flask api

    # add the vehicle_api to the API this isnt really used accept for some early testing
    api.add_namespace(vehicle_api)
    api.add_namespace(mechanic_api)

    @app.route('/vehicles')
    def index(): #load the defult page for seeing our vehicles
        vehicles = Vehicle.get_vehicles()
        # Fetch important dates for each vehicle
        vehicles_with_dates = []
        for vehicle in vehicles:
            dates = ImportantDates.query.filter_by(vehicle_id=vehicle.id).first()
            vehicle_data = vehicle.dict_data()
            if dates:
                vehicle_data['important_dates'] = {
                    'car_tax': dates.car_tax.strftime('%Y-%m-%d') if dates.car_tax else 'N/A',
                    'annual_insurance': dates.annual_insurance.strftime('%Y-%m-%d') if dates.annual_insurance else 'N/A',
                    'technical_review': dates.technical_review.strftime('%Y-%m-%d') if dates.technical_review else 'N/A',
                    'vignette': dates.vignette.strftime('%Y-%m-%d') if dates.vignette else 'N/A',
                    'additional_insurance': dates.additional_insurance.strftime('%Y-%m-%d') if dates.additional_insurance else 'N/A'
                }
            else:
                vehicle_data['important_dates'] = {
                    'car_tax': 'N/A',
                    'annual_insurance': 'N/A',
                    'technical_review': 'N/A',
                    'vignette': 'N/A',
                    'additional_insurance': 'N/A'
                }
            vehicles_with_dates.append(vehicle_data)

        # Save updated data with important dates to JSON file
        with open("src/static/generated/get_vehicles.json", "w") as f:
            f.write(json.dumps(vehicles_with_dates, indent=4))

        # pass vehicles to the template
        return render_template("vehicles.html", vehicles=vehicles_with_dates)

    @app.route('/<vehicle_name>/info')
    def vehicle_info(vehicle_name):
        vehicle = Vehicle.query.filter_by(name=vehicle_name).first()
        dates = ImportantDates.query.filter_by(vehicle_id=vehicle.id).first()
        db.session.close() # this might be a headache
        if vehicle:
            return render_template("vehicle_info.html", vehicle=vehicle, important_dates=dates)
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
        except Exception as e: # Print the error to the console
            print("Error:", str(e))
            return jsonify({'error': 'Failed to save vehicle data'}), 500

    @app.route('/delete_vehicle', methods=['POST']) # now this works
    def delete_vehicle():  # a way to remove the vehicles
        try:
            vehicle_name = request.json.get("name")
            vehicle = Vehicle.query.filter_by(name=vehicle_name).first()
            if vehicle:
                # print(f"Attempting to delete vehicle with ID: {vehicle_id}")
                vehicle.delete_vehicle()
                return jsonify({'message': 'Vehicle deleted successfully'}), 200
            else:
                return jsonify({'error': 'Vehicle not found'}), 404
        except Exception as e:
            # print("Error:", str(e))
            return jsonify({'error': 'Failed to delete vehicle'}), 500

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
                # get the data (make sure its appropariate types)
                amount = float(request.form.get('amount'))
                current_mileage = float(request.form.get('mileage'))
                price_per_liter = float(request.form.get('price_per_liter'))
                total_price = float(request.form.get('total_price'))
                # save the data
                vehicle.refuel(amount, current_mileage, price_per_liter, total_price)
                return redirect(url_for('fuel_vehicle', vehicle_id=vehicle.id))
            except ValueError as e: # handle the errors
                error = str(e)
                refuel_history = RefuelHistory.get_fuel_mileage(vehicle_id)
                return render_template("fuel.html", vehicle=vehicle, error=error, refuel_history=refuel_history)

        if vehicle:
            # give the data so it can be rendered
            refuel_history = RefuelHistory.get_fuel_mileage(vehicle_id)
            return render_template("fuel.html", vehicle=vehicle, refuel_history=refuel_history)
        else:
            return jsonify({'error': 'Vehicle not found'}), 404

    @app.route('/update_refuel/<int:refuel_id>', methods=['GET', 'POST'])
    def update_refuel(refuel_id):
        refuel = RefuelHistory.query.get(refuel_id)
        if request.method == 'POST':
            try:
                data = request.form
                RefuelHistory.update_refuel(refuel_id, data)
                return redirect(url_for('fuel_vehicle', vehicle_id=refuel.vehicle_id))
            except ValueError as e:
                error = str(e)
                return render_template("update_refuel.html", refuel=refuel, error=error)

        return render_template("update_refuel.html", refuel=refuel)

    @app.route('/delete_refuel/<int:refuel_id>', methods=['POST'])
    def delete_refuel(refuel_id):
        vehicle_id = RefuelHistory.delete_refuel(refuel_id)
        if vehicle_id:
            return redirect(url_for('fuel_vehicle', vehicle_id=vehicle_id))
        else:
            return jsonify({'error': 'Refuel record not found'}), 404

    @app.route('/important_dates/<int:vehicle_id>', methods=['GET', 'POST'])
    def important_dates_route(vehicle_id):
        vehicle = Vehicle.query.get(vehicle_id)
        if request.method == 'POST':
            try:
                car_tax = request.form.get('car_tax')
                annual_insurance = request.form.get('annual_insurance')
                technical_review = request.form.get('technical_review')
                vignette = request.form.get('vignette')
                additional_insurance = request.form.get('additional_insurance')

                dates = ImportantDates.update_important_dates(vehicle_id, car_tax, annual_insurance, technical_review, vignette, additional_insurance)

                return redirect(url_for('vehicle_info', vehicle_name=vehicle.name))
            except ValueError as e:
                error = str(e)
                return render_template("important_dates.html", vehicle=vehicle, important_dates=dates, error=error)

        if vehicle:
            dates = ImportantDates.get_important_dates(vehicle_id)
            return render_template("important_dates.html", vehicle=vehicle, important_dates=dates)
        else:
            return jsonify({'error': 'Vehicle not found'}), 404

    @app.route('/mechanics') #addint something to do with the mechanics coz I said I have to
    def mechanics():
        mechanics_data = Mechanic.get_mechanic()
        return render_template("mechanics.html", mechanics=mechanics_data)

    @app.route('/add_mechanic')
    def add_mechanic_form():
        return render_template("add_mechanic.html")

    @app.route('/save_mechanic', methods=['POST'])
    def save_mechanic():
        mechanic_data = request.json
        try:
            new_mechanic = Mechanic(
                id=Mechanic.give_me_id(),
                name=mechanic_data["name"],
                address=mechanic_data["address"],
                email=mechanic_data["email"],
                phone=mechanic_data["phone"],
                hourly_rate=mechanic_data["hourly_rate"],
                note=mechanic_data["note"]
            )
            new_mechanic.add_mechanic()
            return jsonify({'message': 'Mechanic data saved successfully'}), 200
        except Exception as e:
            print("Error:", str(e))
            return jsonify({'error': 'Failed to save mechanic data'}), 500

    @app.route('/edit_mechanic/<int:mechanic_id>', methods=['GET', 'POST'])
    def edit_mechanic(mechanic_id):
        mechanic = Mechanic.query.get(mechanic_id)
        if request.method == 'POST':
            mechanic_data = request.json
            try:
                mechanic.name = mechanic_data["name"]
                mechanic.address = mechanic_data["address"]
                mechanic.email = mechanic_data["email"]
                mechanic.phone = mechanic_data["phone"]
                mechanic.hourly_rate = mechanic_data["hourly_rate"]
                mechanic.note = mechanic_data["note"]
                db.session.commit()
                return jsonify({'message': 'Mechanic updated successfully'}), 200
            except Exception as e:
                print("Error:", str(e))
                return jsonify({'error': 'Failed to update mechanic data'}), 500
        return render_template("edit_mechanic.html", mechanic=mechanic)

    @app.route('/delete_mechanic/<int:mechanic_id>', methods=['POST'])
    def delete_mechanic(mechanic_id):
        try:
            mechanic = Mechanic.query.get(mechanic_id)
            if mechanic:
                mechanic.delete_mechanic()
                return jsonify({'message': 'Mechanic deleted successfully'}), 200
            else:
                return jsonify({'error': 'Mechanic not found'}), 404
        except Exception as e:
            print("Error:", str(e))
            return jsonify({'error': 'Failed to delete mechanic'}), 500

    return app
