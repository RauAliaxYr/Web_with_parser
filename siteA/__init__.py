from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

import config #конфиг файл

app = Flask(__name__)
app.secret_key = config.secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = config.database_root
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
manager = LoginManager(app)

from siteA import models, roots

db.create_all()
