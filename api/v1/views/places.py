from models import storage
from models.city import City
from models.place import Place
from models.user import User
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def retrieve_places_cityid(city_id=None):
    """retrieve places objs of specific city"""

    obj_city = storage.get(City, city_id)

    if obj_city:
        places = []
        for place in obj_city.places:
            places.append(place.to_dict())
        return jsonify(places)
    else:
        abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['GET'])
def retrieve_place(place_id):
    """retreve place given an id"""

    obj = storage.get(Place, place_id)

    if obj:
        obj_todict = obj.to_dict()
        return jsonify(obj_todict), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_place(place_id):
    """Delete a place"""

    obj = storage.get(Place, place_id)

    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['POST'])
def add_place(city_id=None):
    """Add a new place"""

    obj_city = storage.get(City, city_id)
    if obj_city is None:
        abort(404)

    try:
        data = request.get_json()
    except Exception as e:
        abort(400, 'Not a JSON')

    if not data.get('name'):
        abort(400, 'Missing Name')

    if not data.get('user_id'):
        abort(400, 'Missing user_id')

    obj_user = storage.get(User, data.get('user_id'))
    if obj_user is None:
        abort(404)

    new_place = Place(city_id=city_id, user_id=data.get('user_id'), **data)
    storage.new(new_place)
    storage.save()

    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['PUT'])
def update_place(place_id=None):
    """Update info about place"""
    try:
        data = request.get_json()
    except Exception as e:
        abort(400, 'Not a JSON')

    obj = storage.get(Place, place_id)

    if obj:
        for key, value in data.items():
            if key not in ("id", "created_at", "updated_at",
                           'user_id', 'city_id'):
                setattr(obj, key, value)
        storage.save()
    else:
        abort(404)

    return jsonify(obj.to_dict()), 200
