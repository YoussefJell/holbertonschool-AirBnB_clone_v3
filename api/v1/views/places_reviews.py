#!/usr/bin/python3
"""view for Reviews objects that handles all default RESTFul API actions"""
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def retrieve_reviews_placeid(place_id=None):
    """retrieve reviews objs of specific place"""

    obj_place = storage.get(Place, place_id)

    if obj_place:
        reviews = []
        for review in obj_place.reviews:
            reviews.append(review.to_dict())
        return jsonify(reviews)
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['GET'])
def retrieve_reviews(review_id):
    """retreve review given an id"""

    obj = storage.get(Review, review_id)

    if obj:
        obj_todict = obj.to_dict()
        return jsonify(obj_todict), 200
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_review(review_id):
    """Delete a Review"""

    obj = storage.get(Review, review_id)

    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['POST'])
def add_review(place_id=None):
    """Add a new review"""

    obj_place = storage.get(Place, place_id)
    if obj_place is None:
        abort(404)

    try:
        data = request.get_json()
    except Exception as e:
        abort(400, 'Not a JSON')
    if not data.get('user_id'):
        abort(400, 'Missing user_id')
    if not data.get('text'):
        abort(400, 'Missing text')

    user = storage.get(User, data.get('user_id'))

    if user is None:
        abort(404)

    new_review = Review(place_id=place_id, **data)
    storage.new(new_review)
    storage.save()

    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['PUT'])
def update_review(review_id=None):
    """Update info about review"""
    try:
        data = request.get_json()
    except Exception as e:
        abort(400, 'Not a JSON')

    obj = storage.get(Review, review_id)

    if obj:
        for key, value in data.items():
            if key not in ("id", "user_id", "place_id", "created_at", "updated_at"):
                setattr(obj, key, value)
        storage.save()
    else:
        abort(404)

    return jsonify(obj.to_dict()), 200
