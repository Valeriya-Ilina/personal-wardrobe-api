import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict

outfits = Blueprint('outfits', 'outfits')

# "GET" route
@outfits.route('/', methods=['GET'])
def outfits_index():
    #return "get route is working"
    result = models.Outfit.select()
    outfit_list_of_dicts = [model_to_dict(outfit) for outfit in result]

    # convert price Decimal type to string before serializing to JSON
    # to avoid TypeError: Object of type Decimal is not JSON serializable
    for dict_outfit in outfit_list_of_dicts:
        for key, value in dict_outfit['item_id'].items():
            if key == 'price':
                dict_outfit['item_id'][key] = str(value)

    return jsonify({
        'data': outfit_list_of_dicts,
        'message': f"Successfully found {len(outfit_list_of_dicts)} outfits",
        'status': 200
    }), 200


# "POST" route to create an outfit
@outfits.route('/', methods=['POST'])
def create_outfit():
    payload = request.get_json()
    new_outfit = models.Outfit.create(name=payload['name'],date=payload['date'],item_id=payload['item_id'])
    print(new_outfit)

    outfit_dict = model_to_dict(new_outfit)

    for key, value in outfit_dict['item_id'].items():
        if key == 'price':
            outfit_dict['item_id'][key] = str(value)

    return jsonify(
        data=outfit_dict,
        message='Successfully created outfit!',
        status=201
    ), 201


# "SHOW" route
@outfits.route('/<id>', methods=["GET"])
def get_one_outfit(id):
    outfit = models.Outfit.get_by_id(id)
    outfit_dict = model_to_dict(outfit)
    for key, value in outfit_dict['item_id'].items():
        if key == 'price':
            outfit_dict['item_id'][key] = str(value)

    return jsonify(
        data = outfit_dict,
        message = 'Outfit is found',
        status = 200
    ), 200


# "PUT" route to update an outfit
@outfits.route('/<id>', methods=["PUT"])
def update_outfit(id):
    payload = request.get_json()
    # update data in DB
    models.Outfit.update(**payload).where(models.Outfit.id==id).execute()

    # GET updated data from DB
    outfit = models.Outfit.get_by_id(id)
    outfit_dict = model_to_dict(outfit)
    for key, value in outfit_dict['item_id'].items():
        if key == 'price':
            outfit_dict['item_id'][key] = str(value)

    return jsonify(
        data = outfit_dict,
        status = 200,
        message = 'Resource updated seccessfully'
    ), 200


# "DELETE" route
@outfits.route('/<id>', methods=["DELETE"])
def delete_outfit(id):
    models.Outfit.delete().where(models.Outfit.id==id).execute()

    return jsonify(
        data = None,
        status = 200,
        message = 'Resource deleted seccessfully'
    ), 200
