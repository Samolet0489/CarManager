import json
from random import randint

from src.database import db

class Mechanic(db.Model):
    # table name in the database
    __tablename__ = 'mechanic'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)  # mechanic's name
    address = db.Column(db.String(80), nullable=False)  # mechanic's address
    email = db.Column(db.String(80), nullable=False)  # mechanic's email
    phone = db.Column(db.String(80), nullable=False)  # mechanic's phone number
    hourly_rate = db.Column(db.Float, nullable=False)  # mechanic's hourly rate
    note = db.Column(db.Text, nullable=True)  # additional notes about the mechanic


    def __init__(self, id:int, name:str, address:str,email:str, phone:str, hourly_rate:float, note:str):
        self.id = id
        self.name = name
        self.address = address
        self.email = email
        self.phone = phone
        self.hourly_rate = hourly_rate
        self.note = note
        # consider adding contacts instead of checking availability through the app

    def dict_data(self):
        # convert mechanic details to dictionary format
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'email': self.email,
            'phone': self.phone,
            'hourly_rate': self.hourly_rate,
            'note': self.note,
        }

    @staticmethod
    def give_me_id(): # doesnt really need to be random id, might be better if there is no random
        try:            # this is a problem for future me to decide on
            ids = [mechanic.id for mechanic in Mechanic.query.all()]
            # print(ids)
            # print(type(ids[0]))
            new_id  = randint(0,99999999999)
            while new_id  in ids:
                new_id  = randint(0, 99999999999)
            return new_id
        except Exception as e:
            print("Error:", e)
            return 0


    def add_mechanic(self):
        # add a new mechanic to the database
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_mechanic():
        # retrieve all mechanics from the database
        data = Mechanic.query.all()
        mechanic_json = [m.dict_data() for m in data]

        # save mechanic data to a JSON file
        with open("src/static/generated/mechanic.json", "w") as f:
            f.write(json.dumps(mechanic_json, indent=4))

        return data

    def delete_mechanic(self):
        # delete a mechanic from the database
        db.session.delete(self)
        db.session.commit()

    def get_mechanic_id(self, id):
        # retrieve a specific mechanic by ID
        data = Mechanic.query.filter_by(id=id).first()
        return data

    def is_busy(self):
        #check if the mechanic is busy
        pass
