from flask import Flask
from flask_restx import Api

#import the NS models here (NS might stand fir newspaper so rename?)


def create_app():
    app = Flask(__name__)
    api = Api(app) #  title= you can add a name

    # you have to add the namespace so flask will see the module

    #app.add_namespace(MYAPI)

    return app

if __name__ == '__main__':
    create_app().run(debug=False, port=5000) # see if you want to change the port