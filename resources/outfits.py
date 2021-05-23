import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required

outfits = Blueprint('outfits', 'outfits')

# "GET" route
@outfits.route('/', methods=['GET'])
@login_required
def outfits_index():
    #return "get route is working"
    outfit_list_of_dicts = [model_to_dict(outfit) for outfit in current_user.user_outfits]
    print(outfit_list_of_dicts)

    # convert price Decimal type to string before serializing to JSON
    # to avoid TypeError: Object of type Decimal is not JSON serializable
    # for dict_outfit in outfit_list_of_dicts:
    #     for key, value in dict_outfit['item_id'].items():
    #         if key == 'price':
    #             dict_outfit['item_id'][key] = str(value)

    # remove user data
    for outfit_dict in outfit_list_of_dicts:
        outfit_dict.pop('user_id')

    return jsonify({
        'data': outfit_list_of_dicts,
        'message': f"Successfully found {len(outfit_list_of_dicts)} outfits",
        'status': 200
    }), 200


# "POST" route to create an outfit
@outfits.route('/', methods=['POST'])
@login_required
def create_outfit():
    payload = request.get_json()
    new_outfit = models.Outfit.create(name=payload['name'],user_id=current_user.id,date=payload['date'])
    print(new_outfit)

    outfit_dict = model_to_dict(new_outfit)

    # for key, value in outfit_dict['item_id'].items():
    #     if key == 'price':
    #         outfit_dict['item_id'][key] = str(value)
    #
    # # remove user data
    # dict_outfit['item_id'].pop('user_id')

    return jsonify(
        data=outfit_dict,
        message='Successfully created outfit!',
        status=201
    ), 201


# "SHOW" route
@outfits.route('/<id>', methods=["GET"])
@login_required
def get_one_outfit(id):
    outfit = models.Outfit.get_by_id(id)
    outfit_dict = model_to_dict(outfit)
    # for key, value in outfit_dict['item_id'].items():
    #     if key == 'price':
    #         outfit_dict['item_id'][key] = str(value)

    # remove user data
    outfit_dict.pop('user_id')

    return jsonify(
        data = outfit_dict,
        message = 'Outfit is found',
        status = 200
    ), 200


# "PUT" route to update an outfit
@outfits.route('/<id>', methods=["PUT"])
@login_required
def update_outfit(id):
    payload = request.get_json()
    # update data in DB
    models.Outfit.update(**payload).where(models.Outfit.id==id).execute()

    # GET updated data from DB
    outfit = models.Outfit.get_by_id(id)
    outfit_dict = model_to_dict(outfit)
    # for key, value in outfit_dict['item_id'].items():
    #     if key == 'price':
    #         outfit_dict['item_id'][key] = str(value)

    # remove user data
    outfit_dict.pop('user_id')

    return jsonify(
        data = outfit_dict,
        status = 200,
        message = 'Resource updated seccessfully'
    ), 200


# "DELETE" route
@outfits.route('/<id>', methods=["DELETE"])
@login_required
def delete_outfit(id):
    models.Outfit.delete().where(models.Outfit.id==id).execute()

    return jsonify(
        data = None,
        status = 200,
        message = 'Resource deleted seccessfully'
    ), 200
