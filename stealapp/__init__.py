from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

from stealapp import config
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
app.config.from_object(config.LiveConfig)
db = SQLAlchemy(app)
csrf = CSRFProtect(app)
from stealapp import routes,models
from stealapp.routes import user_routes,admin_routes,store_routes

