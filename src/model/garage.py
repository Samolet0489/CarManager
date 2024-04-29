from typing import List, Union, Optional
from .vehicle import Vehicle
from ..database import db

# here can be the main logic of the app

class Garage(db.Model):
    singleton_instance = None # see if you actually need this




    def __init__(self):
        self.vehicles: List[Vehicle] = []






