from flask import Flask
import models

import os
from dotenv import load_dotenv
load_dotenv()

DEBUG=True
PORT=8000

app = Flask(__name__)

app.secret_key = os.environ.get("FLASK_APP_SECRET")

@app.route('/')
def hello():
    return 'Hello, Wardrobe!'




if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
