#!/usr/bin/python3
"""
route that returns json status response
"""
from api.v1.views import app_views
from flask import jsonify, request


@app_views.route('/status', methods=['GET'])
def send_status():
    """returns the status"""

    if request.method == "GET":
        response = {'status': 'OK'}
    return jsonify(response)
