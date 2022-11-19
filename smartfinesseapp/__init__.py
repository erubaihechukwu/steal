from flask import Flask
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_migrate import Migrate

from smartfinesseapp import config
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
app.config.from_object(config.LiveConfig)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)
from smartfinesseapp import routes,models
from smartfinesseapp.routes import user_routes,admin_routes,store_routes

