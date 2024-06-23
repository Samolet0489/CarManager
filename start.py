from src.app import create_app

# start the application
if __name__ == '__main__':
    # create the Flask application
    app = create_app()
    # run the application on port 5000 with debug mode disabled
    create_app().run(debug=False, port=5000)
