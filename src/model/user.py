from src.database import db
from random import randint

# here we are going to have to add a user system
# (we dont need much info: id, Name/nickname, password/key)
# make it so that after someone connects with an acc then they can change their specific value
# now there is a reason to have the randint id system
class User (db.Model):

        # connect the user to the vehicle table but make it so that every vehicle has its own user
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    # this should be enough for our needs

    def __init__(self, id:int, name:str, password:str):
        self.id = id # this should be created with the give_me_id()
        self.name = name
        self.password = password
        # self.cars = [] # make a list with the Ids of the cars that the person owns so that we can access the
                            # already existing databases

        # connect the vehicle table to the user somehow?


    @staticmethod
    def give_me_id():
        try:
            ids = [vehicle.id for vehicle in User.query.all()] # we retrieve the IDs
            # print(ids)
            # print(type(ids[0]))
            new_id  = randint(0,99999999999)
            while new_id  in ids:
                new_id  = randint(0, 99999999999)
            return new_id
        except Exception as e:
            print("Error:", e)
            return 0

