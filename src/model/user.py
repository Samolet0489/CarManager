from src.database import db
from random import randint

# here we are going to have to add a user system
# (we dont need much info: id, Name/nickname, password/key)
# make it so that after someone connects with an acc then they can change their specific value
# now there is a reason to have the randint id system
class User (db.Model):

        # connect the user to the vehicle table but make it so that every vehicle has its own user
    __tablename__ = 'user'

    # Define the columns for the user table
    id = db.Column(db.Integer, primary_key=True) # id for the user (has to be unique)
    name = db.Column(db.String(80), unique=True, nullable=False)  # name for the  user
    password = db.Column(db.String(80), nullable=False) # user password
    # this should be enough for our needs

    def __init__(self, id:int, name:str, password:str):
        self.id = id # this should be created with the give_me_id()
        self.name = name
        self.password = password
        # self.cars = [] # make a list with the Ids of the cars that the person owns so that we can access the
                            # already existing databases

        # connect the vehicle table to the user somehow?

    # static method to generate a unique user ID
    @staticmethod
    def give_me_id():
        try:
            # get the existing Ids
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

    def add_user(self): # add users to the DB
        db.session.add(self)
        db.session.commit()

    def delete_user(self): # remove users from the DB
        db.session.delete(self)
        db.session.commit()

    # Method to edit user details
    def edit_user(self, id:int, name:str, password:str):
        user = User.query.get(id)
        user.name = name
        user.password = password
        db.session.commit()


