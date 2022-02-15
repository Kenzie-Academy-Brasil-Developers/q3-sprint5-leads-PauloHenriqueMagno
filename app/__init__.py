from flask import Flask
from environs import Env
from app.configs import database, migrations
from app import routes

def create_app():
  app = Flask(__name__)

  env = Env()
  env.read_env()

  app.config["SQLALCHEMY_DATABASE_URI"] = env("SQLALCHEMY_DATABASE_URI")
  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
  app.config['JSON_SORT_KEYS'] = False

  database.init_app(app)
  migrations.init_app(app)
  routes.init_app(app)

  return app