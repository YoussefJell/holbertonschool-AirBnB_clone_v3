from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route('/amenities', strict_slashes=False,
                 methods=['GET'])
@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET'])
def retrieve_amenity(amenity_id=None):
    """retrieve amenities objs"""
    dict_objs = storage.all(Amenity)

    if amenity_id is None:
        all_objs = [obj.to_dict() for obj in dict_objs.values()]
        return jsonify(all_objs)

    obj = dict_objs.get('Amenity.{}'.format(amenity_id))

    if obj:
        obj_todict = obj.to_dict()
        return jsonify(obj_todict)
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_amenity(amenity_id=None):
    """Delete an amenity """
    dict_objs = storage.all(Amenity)

    obj = dict_objs.get('Amenity.{}'.format(amenity_id))

    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/amenities', strict_slashes=False,
                 methods=['POST'])
def add_amenity():
    """Add a new amenity"""
    data = request.get_json(force=True, silent=True)

    if data is None:
        abort(400, 'Not a JSON')
    if not data.get('name'):
        abort(400, 'Missing Name')

    new_amenity = Amenity(**data)
    storage.new(new_amenity)
    storage.save()

    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['PUT'])
def update_amenity(amenity_id=None):
    """Update info about an amenity"""
    data = request.get_json(force=True, silent=True)

    if data is None:
        abort(400, 'Not a JSON')

    dict_objs = storage.all(Amenity)

    obj = dict_objs.get('Amenity.{}'.format(amenity_id))

    if obj:
        for k, v in data.items():
            if k == 'id' or k == 'created_at' or k == 'updated_at':
                continue
            setattr(obj, k, v)
        storage.save()
    else:
        abort(404)

    return jsonify(obj.to_dict()), 200
