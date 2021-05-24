import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required

outfit_collections = Blueprint('outfit_collections', 'outfit_collections')


# "GET" route
@outfit_collections.route('/', methods=['GET'])
@login_required
def outfit_collections_index():
    result = models.Outfit_Collection.select().join(models.Outfit).where(models.Outfit.user_id == current_user.id)
    outfit_collection_list_of_dicts = [model_to_dict(outfit_collection) for outfit_collection in result]

    # convert price Decimal type to string before serializing to JSON
    # to avoid TypeError: Object of type Decimal is not JSON serializable
    print(outfit_collection_list_of_dicts)
    for outfit_collection_dict in outfit_collection_list_of_dicts:
        for key, value in outfit_collection_dict['item_id'].items():
            if key == 'price':
                outfit_collection_dict['item_id'][key] = str(value)

    # remove user data
    for outfit_collection_dict in outfit_collection_list_of_dicts:
        outfit_collection_dict['item_id'].pop('user_id')
        outfit_collection_dict['outfit_id'].pop('user_id')

    return jsonify({
        'data': outfit_collection_list_of_dicts,
        'message': f"Successfully found {len(outfit_collection_list_of_dicts)} items",
        'status': 200
    }), 200


# "POST" route
@outfit_collections.route('/', methods=['POST'])
@login_required
def create_outfit_collections():
    payload = request.get_json()
    new_outfit_collection = models.Outfit_Collection.create(item_id=payload['item_id'], outfit_id=payload['outfit_id'], coordinateX=payload['coordinateX'], coordinateY=payload['coordinateY'], image_width=payload['image_width'], image_height=payload['image_height'])
    print(new_outfit_collection)

    # convert price Decimal type to string before serializing to JSON
    # to avoid TypeError: Object of type Decimal is not JSON serializable
    for key, value in new_outfit_collection.items():
        if key == 'price':
            outfit_collection_dict[key] = str(value)

    # remove user data
    outfit_collection_dict['item_id'].pop('user_id')
    outfit_collection_dict['outfit_id'].pop('user_id')

    outfit_collection_dict = model_to_dict(new_outfit_collection)

    return jsonify(
        data=outfit_collection_dict,
        message='Successfully created outfit collection!',
        status=201
    ), 201


# "SHOW" route
@outfit_collections.route('/<id>', methods=["GET"])
@login_required
def get_one_outfit_collection(id):
    outfit_collection = models.Outfit_Collection.get_by_id(id)
    outfit_collection_dict = model_to_dict(outfit_collection)

    for key, value in outfit_collection_dict['item_id'].items():
        if key == 'price':
            outfit_collection_dict['item_id'][key] = str(value)

    # remove user data
    outfit_collection_dict['item_id'].pop('user_id')
    outfit_collection_dict['outfit_id'].pop('user_id')

    return jsonify(
        data = outfit_collection_dict,
        message = 'Outfit is found',
        status = 200
    ), 200


# "PUT" route to update an outfit_collection
@outfit_collections.route('/<id>', methods=["PUT"])
@login_required
def update_outfit_collection(id):
    payload = request.get_json()
    # update data in DB
    models.Outfit_Collection.update(**payload).where(models.Outfit_Collection.id==id).execute()

    # GET updated data from DB
    outfit_collection = models.Outfit_Collection.get_by_id(id)
    outfit_collection_dict = model_to_dict(outfit_collection)

    for key, value in outfit_collection_dict['item_id'].items():
        if key == 'price':
            outfit_collection_dict['item_id'][key] = str(value)

    # remove user data
    outfit_collection_dict['item_id'].pop('user_id')
    outfit_collection_dict['outfit_id'].pop('user_id')

    return jsonify(
        data = outfit_collection_dict,
        status = 200,
        message = 'Resource updated seccessfully'
    ), 200


# "DELETE" route
@outfit_collections.route('/<id>', methods=["DELETE"])
@login_required
def delete_outfit_collection(id):
    models.Outfit_Collection.delete().where(models.Outfit_Collection.id==id).execute()

    return jsonify(
        data = None,
        status = 200,
        message = 'Resource deleted seccessfully'
    ), 200
