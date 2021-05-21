import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_bcrypt import generate_password_hash

users = Blueprint('users','users')

@users.route('/', methods=['GET'])
def test_user_resource():
    result = models.User_Account.select()
    user_list_of_dicts = [model_to_dict(user) for user in result]
    return jsonify(
        data=user_list_of_dicts,
        message=f"Successfully found {len(user_list_of_dicts)} users",
        status=200
    ), 200

@users.route('/', methods=['POST'])
def register():
    payload = request.get_json()
    payload['email'] = payload['email'].lower()
    payload['username'] = payload['username'].lower()
    try:
        models.User_Account.get(models.User_Account.email == payload['email'])
        return jsonify(
            data={},
            message=f"User with email {payload['email']} already exists",
            status=401
        ), 401
    except models.DoesNotExist:
        pw_hash = generate_password_hash(payload['password'])

        created_user = models.User_Account.create(
            username=payload['username'],
            email=payload['email'],
            password=pw_hash
        )
        created_user_dict = model_to_dict(created_user)
        created_user_dict.pop('password')

        return jsonify(
            data=created_user_dict,
            message=f"Successfully registered user {created_user_dict['email']}",
            status=201
        ), 201
