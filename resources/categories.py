import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required

categories = Blueprint('categories', 'categories')

# "GET" route
@categories.route('/', methods=['GET'])
@login_required
def categories_index():
    result = models.Category.select()
    category_list_of_dicts = [model_to_dict(category) for category in result]

    for category_dict in category_list_of_dicts:
        for key, value in category_dict['item_id'].items():
            if key == 'price':
                category_dict['item_id'][key] = str(value)

    return jsonify({
        'data': category_list_of_dicts,
        'message': f"Successfully found {len(category_list_of_dicts)} categories",
        'status': 200
    }), 200


# "POST" route to create a category
@categories.route('/', methods=['POST'])
@login_required
def create_category():
    payload = request.get_json()
    new_category = models.Category.create(name=payload['name'],item_id=payload['item_id'])
    print(new_category)

    category_dict = model_to_dict(new_category)

    for key, value in category_dict['item_id'].items():
        if key == 'price':
            category_dict['item_id'][key] = str(value)

    return jsonify(
        data=category_dict,
        message='Successfully created category!',
        status=201
    ), 201


# "SHOW" route
@categories.route('/<id>', methods=["GET"])
@login_required
def get_one_category(id):
    category = models.Category.get_by_id(id)
    category_dict = model_to_dict(category)
    for key, value in category_dict['item_id'].items():
        if key == 'price':
            category_dict['item_id'][key] = str(value)

    return jsonify(
        data = category_dict,
        message = 'Category is found',
        status = 200
    ), 200


# "PUT" route to update a category
@categories.route('/<id>', methods=["PUT"])
@login_required
def update_category(id):
    payload = request.get_json()
    # update data in DB
    models.Category.update(**payload).where(models.Category.id==id).execute()

    # GET updated data from DB
    category = models.Category.get_by_id(id)
    category_dict = model_to_dict(category)
    for key, value in category_dict['item_id'].items():
        if key == 'price':
            category_dict['item_id'][key] = str(value)

    return jsonify(
        data = category_dict,
        status = 200,
        message = 'Resource updated seccessfully'
    ), 200

# "DELETE" route
@categories.route('/<id>', methods=["DELETE"])
@login_required
def delete_category(id):
    models.Category.delete().where(models.Category.id==id).execute()

    return jsonify(
        data = None,
        status = 200,
        message = 'Resource deleted seccessfully'
    ), 200
