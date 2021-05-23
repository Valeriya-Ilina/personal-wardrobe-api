import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required

items = Blueprint('items', 'items')

# "GET" route
@items.route('/', methods=['GET'])
@login_required
def items_index():
    item_list_of_dicts = [model_to_dict(item) for item in current_user.user_items]

    # convert price Decimal type to string before serializing to JSON
    # to avoid TypeError: Object of type Decimal is not JSON serializable
    for dict_item in item_list_of_dicts:
        for key, value in dict_item.items():
            if key == 'price':
                dict_item[key] = str(value)

    return jsonify({
        'data': item_list_of_dicts,
        'message': f"Successfully found {len(item_list_of_dicts)} items",
        'status': 200
    }), 200

# "POST" route to create an item
@items.route('/', methods=['POST'])
@login_required
def create_item():
    payload = request.get_json()
    new_item = models.Item.create(name=payload['name'],price=payload['price'],user_id=current_user.id,url=payload['url'])
    print(new_item)

    item_dict = model_to_dict(new_item)

    return jsonify(
        data=item_dict,
        message='Successfully created item!',
        status=201
    ), 201

# "SHOW" route
@items.route('/<id>', methods=["GET"])
@login_required
def get_one_item(id):
    item = models.Item.get_by_id(id)
    item_dict = model_to_dict(item)
    for key, value in item_dict.items():
        if key == 'price':
            item_dict[key] = str(value)

    return jsonify(
        data = item_dict,
        message = 'Item is found',
        status = 200
    ), 200

# "PUT" route to update an item
@items.route('/<id>', methods=["PUT"])
@login_required
def update_item(id):
    payload = request.get_json()
    # update data in DB
    models.Item.update(**payload).where(models.Item.id==id).execute()

    # GET updated data from DB
    item = models.Item.get_by_id(id)
    item_dict = model_to_dict(item)
    for key, value in item_dict.items():
        if key == 'price':
            item_dict[key] = str(value)

    return jsonify(
        data = item_dict,
        status = 200,
        message = 'Resource updated seccessfully'
    ), 200

# "DELETE" route
@items.route('/<id>', methods=["DELETE"])
@login_required
def delete_item(id):
    models.Item.delete().where(models.Item.id==id).execute()

    return jsonify(
        data = None,
        status = 200,
        message = 'Resource deleted seccessfully'
    ), 200
