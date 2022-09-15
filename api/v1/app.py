#!/usr/bin/python3
"""starts a Flask web application"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exc):
    """close the storage instance"""
    storage.close()


if __name__ == "__main__":
    if getenv('HBNB_API_HOST') is None:
        HBNB_API_HOST = '0.0.0.0'

    if getenv('HBNB_API_PORT') is None:
        HBNB_API_PORT = 5000

    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
