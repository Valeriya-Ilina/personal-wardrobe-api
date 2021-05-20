import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict

items = Blueprint('items', 'items')

# "GET" route
@items.route('/', methods=['GET'])
def items_index():
    #return "get route is working"
    result = models.Item.select()
    item_list_of_dicts = [model_to_dict(item) for item in result]

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
def create_item():
    payload = request.get_json()
    new_item = models.Item.create(name=payload['name'],price=payload['price'],user_id=payload['user_id'],url=payload['url'])
    print(new_item)

    item_dict = model_to_dict(new_item)

    return jsonify(
        data=item_dict,
        message='Successfully created item!',
        status=201
    ), 201
