#!/usr/bin/python3
"""
route that returns json status response
"""
from api.v1.views import app_views
from flask import jsonify, request
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route('/status', methods=['GET'])
def send_status():
    """returns the status"""

    if request.method == "GET":
        response = {'status': 'OK'}
    return jsonify(response)


@app_views.route('/stats')
def show_stats():
    """returns the count for all objects"""
    all_counts = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }
    return jsonify(all_counts)


@app_views.app_errorhandler(404)
def not_found(e):
    """Page not found."""
    response = {"error": "Not found"}
    return jsonify(response), e.code
