from flask import Flask
from app.routes.leads_route import bp_leads

def init_app(app: Flask):

  app.register_blueprint(bp_leads)