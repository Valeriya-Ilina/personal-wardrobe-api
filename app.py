from flask import Flask
import models
from resources.items import items
from resources.categories import categories
from resources.outfits import outfits
from resources.users import users
import os
from dotenv import load_dotenv
load_dotenv()

DEBUG=True
PORT=8000

app = Flask(__name__)

app.secret_key = os.environ.get("FLASK_APP_SECRET")

app.register_blueprint(items, url_prefix='/api/v1/items')
app.register_blueprint(categories, url_prefix='/api/v1/categories')
app.register_blueprint(outfits, url_prefix='/api/v1/outfits')
app.register_blueprint(users, url_prefix='/api/v1/users')

@app.route('/')
def hello():
    return 'Hello, Wardrobe!'


if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
