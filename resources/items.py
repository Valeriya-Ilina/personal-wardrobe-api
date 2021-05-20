import models
from flask import Blueprint


items = Blueprint('items', 'items')

@items.route('/', methods=['GET'])
def items_index():
    return "get route is working"
