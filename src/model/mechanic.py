import json
from random import randint

from src.database import db

class Mechanic(db.Model):

    # making a table for the mechanic
    __tablename__ = 'mechanic'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),  nullable=False)
    address = db.Column(db.String(80),  nullable=False)
    email = db.Column(db.String(80),  nullable=False)
    phone = db.Column(db.String(80),  nullable=False)
    hourly_rate = db.Column(db.Float, nullable=False)
    note = db.Column(db.Text, nullable=True) # this is changed from the originally submitted as it made no sence to have it


    def __init__(self, id:int, name:str, address:str,email:str, phone:str, hourly_rate:float, note:str):
        self.id = id
        self.name = name
        self.address = address
        self.email = email
        self.phone = phone
        self.hourly_rate = hourly_rate
        self.note = note
        #better add contacts or smth rather than when he is busy coz we will have to call him to decide if he is busy or not
        # the app has no way to know that accept ofc if the mechanic is not dependent on the app (was not planning on that)


        # add more if needed but dont forget to add them in the db if you do


    def dict_data(self):
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
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_mechanic(): #I will most likely have to get a specific mechanic
        data = Mechanic.query.all()
        mechanic_json = [m.dict_data() for m in data]

        with open("src/static/generated/mechanic.json", "w") as f:
            f.write(json.dumps(mechanic_json, indent=4))

        return data

    def delete_mechanic(self):
        db.session.delete(self)
        db.session.commit()

    def get_mechanic_id(self, id):
        data = Mechanic.query.filter_by(id=id).first()
        return data

    def is_busy(self):
        #check if the mechanic is busy
        pass