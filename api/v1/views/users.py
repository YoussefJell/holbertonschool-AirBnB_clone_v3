#!/usr/bin/python3
"""view for User objects that handles all default RESTFul API actions"""
from models import storage
from models.user import User
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route('/users', strict_slashes=False,
                 methods=['GET'])
@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['GET'])
def retrieve_user(user_id=None):
    """retrieve user objs"""
    dict_objs = storage.all(User)

    if user_id is None:
        all_objs = [obj.to_dict() for obj in dict_objs.values()]
        return jsonify(all_objs)

    obj = storage.get(User, user_id)

    if obj:
        obj_todict = obj.to_dict()
        return jsonify(obj_todict)
    else:
        abort(404)


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_user(user_id):
    """Delete a user"""

    obj = storage.get(User, user_id)

    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users/', strict_slashes=False,
                 methods=['POST'])
def add_user():
    """Add a new user"""
    try:
        data = request.get_json()
    except Exception as e:
        abort(400, 'Not a JSON')
    if not data.get('email'):
        abort(400, 'Missing email')
    if not data.get('password'):
        abort(400, 'Missing password')

    new_user = User(**data)
    storage.new(new_user)
    storage.save()

    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['PUT'])
def update_user(user_id=None):
    """Update info about user"""
    try:
        data = request.get_json()
    except Exception as e:
        abort(400, 'Not a JSON')

    obj = storage.get(User, user_id)

    if obj:
        for key, value in data.items():
            if key not in ("id", "user", "created_at", "updated_at"):
                setattr(obj, key, value)
        storage.save()
    else:
        abort(404)

    return jsonify(obj.to_dict()), 200
