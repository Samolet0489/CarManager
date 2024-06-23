
# Vehicle Management System

The Vehicle Management System is a web application designed to manage and maintain information about vehicles, 
including their fuel history, important dates, oil status, and associated mechanics. This project utilizes Flask for 
the backend, SQLAlchemy for database management, and Flask-RESTx for API management. The frontend is built using HTML and CSS.

## Features

- Add, edit, and delete vehicles.
- Record and update fuel refueling history.
- Maintain important dates related to each vehicle (e.g., car tax, insurance, technical review).
- Record and update oil change statuses.
- Manage information about associated mechanics.

## Directory Structure


    .
    ├── src/
    │   ├── app.py
    │   ├── database.py
    │   ├── model/
    │   │   ├── important_dates.py
    │   │   ├── mechanic.py
    │   │   ├── refuel_history.py
    │   │   └── vehicle.py
    │   ├── api/
    │   │   ├── vehicleG.py
    │   │   └── mechanicG.py
    │   └── static/
    │       ├── generated/
    │       └── styles.css
    ├── templates/
    │   ├── create_vehicle.html
    │   ├── edit_specific_oil_status.html
    │   ├── edit_oil_status.html
    │   ├── edit_vehicle.html
    │   ├── fuel.html
    │   ├── important_dates.html
    │   ├── update_refuel.html
    │   ├── vehicle_info.html
    │   └── vehicles.html
    ├── tests/
    │   ├── test_app.py
    │   ├── test_fuel.py
    │   ├── test_important_dates.py
    │   ├── test_mechanic.py
    │   ├── test_vehicle.py
    │   └── test_vehicleG.py
    ├── .env
    ├── .gitignore
    ├── pytest.ini
    ├── requirements.txt
    ├── start.py
    └── README.md


## Installation

### Prerequisites

- Python 3.12.4 or higher
- Virtualenv

### Steps

Clone the repository:

```bash
git clone https://github.com/yourusername/vehicle-management-system.git
cd vehicle-management-system
```

Create a virtual environment and activate it:

```bash
python -m venv .venv
.venv\Scripts\activate  # On Windows
source .venv/bin/activate  # On Unix or MacOS
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Set up the database (sometimes this step can be skipped):

```bash
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

Run the application:

```bash
python start.py
```

Open your browser and navigate to [http://127.0.0.1:5000/vehicles](http://127.0.0.1:5000/vehicles)

## Running Tests

Before you start, execute:

```bash
$env:PYTHONPATH = ".;./src"
```

To run the tests, simply execute:

```bash
pytest
```

This will run all tests in the tests directory and provide you with a summary of the test results.

## API Endpoints

### Vehicle API

- `POST /api/vehicle/` - Create a new vehicle
- `GET /api/vehicle/` - Get all vehicles
- `PUT /api/vehicle/<id>` - Update a vehicle
- `DELETE /api/vehicle/<id>` - Delete a vehicle

### Mechanic API

- `POST /api/mechanic/` - Create a new mechanic
- `GET /api/mechanic/` - Get all mechanics
- `DELETE /api/mechanic/<id>` - Delete a mechanic

## Frontend Pages

- `/vehicles` - View all vehicles
- `/vehicle/<id>/info` - View vehicle information
- `/add` - Add a new vehicle
- `/edit_vehicle/<id>` - Edit vehicle details
- `/fuel_vehicle/<id>` - View and update fuel history
- `/update_refuel/<id>` - Update a specific refuel entry
- `/important_dates/<id>` - View and edit important dates
- `/mechanics` - View all mechanics
- `/add_mechanic` - Add a new mechanic

## License

This project is licensed under the MIT License. See the LICENSE file for details.


### Pointless files or dead code?!?!?
- There are some things that are not implemented.
Code that is not quite cleaned up and etc. Please disregard those as
In the sommer I am looking forward to implementing some other features and trying things
with this project. I understand that this leaves a bit of a mess but if the project is used the way it is supposed
to be it is not noticeable as all the "To be implemented" features are disconnected from the user (potential customer)
of the project. 

