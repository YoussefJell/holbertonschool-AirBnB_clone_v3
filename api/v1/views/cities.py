from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def retrieve_cities_stateid(state_id=None):
    """retrieve cities objs of specific state"""
    dict_objs = storage.all(State)

    obj_state = dict_objs.get('State.{}'.format(state_id))

    if obj_state:
        cities = []
        for city in obj_state.cities:
            cities.append(city.to_dict())
        return jsonify(cities)
    else:
        abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['GET'])
def retrieve_cities(city_id):
    """retreve city given an id"""
    dict_objs = storage.all(City)

    obj = dict_objs.get('City.{}'.format(city_id))

    if obj:
        obj_todict = obj.to_dict()
        return jsonify(obj_todict), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_city(city_id):
    """Delete a city"""
    dict_objs = storage.all(City)

    obj = dict_objs.get('City.{}'.format(city_id))

    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['POST'])
def add_city(state_id=None):
    """Add a new city"""

    dict_objs = storage.all(State)

    obj_state = dict_objs.get('State.{}'.format(state_id))
    if not obj_state:
        abort(404)

    data = request.get_json(force=True, silent=True)

    if data is None:
        abort(400, 'Not a JSON')
    if not data.get('name'):
        abort(400, 'Missing Name')

    new_city = City(state_id=state_id, **data)
    storage.new(new_city)
    storage.save()

    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['PUT'])
def update_city(city_id=None):
    """Update info about city"""
    data = request.get_json(force=True, silent=True)

    if data is None:
        abort(400, 'Not a JSON')

    dict_objs = storage.all(City)

    obj = dict_objs.get('City.{}'.format(city_id))

    if obj:
        for k, v in data.items():
            if k == 'id' or k == 'created_at' or k == 'updated_at':
                continue
            setattr(obj, k, v)
        storage.save()
    else:
        abort(404)

    return jsonify(obj.to_dict()), 200
