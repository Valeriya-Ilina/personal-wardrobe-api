from flask import Flask, render_template, request, jsonify
import models
from resources.items import items
from resources.categories import categories
from resources.outfits import outfits
from resources.users import users
from resources.outfit_collections import outfit_collections
from flask_cors import CORS
from flask_login import LoginManager
import os
from dotenv import load_dotenv

from cloudinary import config
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url

load_dotenv()

DEBUG=True
PORT=8000

app = Flask(__name__)

app.secret_key = os.environ.get("FLASK_APP_SECRET")
login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return models.User_Account.get(models.User_Account.id == user_id)

CORS(items, origins=['http://localhost:3000'], supports_credentials=True)
CORS(users, origins=['http://localhost:3000'], supports_credentials=True)
CORS(categories, origins=['http://localhost:3000'], supports_credentials=True)
CORS(outfits, origins=['http://localhost:3000'], supports_credentials=True)
CORS(outfit_collections, origins=['http://localhost:3000'], supports_credentials=True)

app.register_blueprint(items, url_prefix='/api/v1/items')
app.register_blueprint(categories, url_prefix='/api/v1/categories')
app.register_blueprint(outfits, url_prefix='/api/v1/outfits')
app.register_blueprint(users, url_prefix='/api/v1/users')
app.register_blueprint(outfit_collections, url_prefix='/api/v1/outfit-collections')


@app.route('/')
def hello():
    return 'Hello, Wardrobe!'


config(
    cloud_name = os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key = os.environ.get("CLOUDINARY_APIKEY"),
    api_secret = os.environ.get("CLOUDINARY_API_SECRET")
)
@app.route('/cloudinary/', methods=['GET', 'POST'])
def upload_file():
    upload("https://img.ltwebstatic.com/images3_pi/2020/04/16/15870362237f09c0e2eddf201834b7fec29db61725_thumbnail_900x.webp", public_id = "sample_dress")
    return jsonify({
        'data': None,
        'message': f"Successfully upload image",
        'status': 200
    }), 200

    # upload_result = None
    # thumbnail_url1 = None
    # thumbnail_url2 = None
    # if request.method == 'POST':
    #     file_to_upload = request.files['file']
    #     if file_to_upload:
    #         upload_result = upload(file_to_upload)
    #         thumbnail_url1, options = cloudinary_url(upload_result['public_id'], format="jpg", crop="fill", width=100,
    #                                                  height=100)
    #         thumbnail_url2, options = cloudinary_url(upload_result['public_id'], format="jpg", crop="fill", width=200,
    #                                                  height=100, radius=20, effect="sepia")
    # return render_template('upload_form.html', upload_result=upload_result, thumbnail_url1=thumbnail_url1,
    #                        thumbnail_url2=thumbnail_url2)


if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
