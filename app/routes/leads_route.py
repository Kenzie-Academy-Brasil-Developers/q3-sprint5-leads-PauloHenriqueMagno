from termios import NL1
from flask import Blueprint
from app.controllers import leads_controller

bp_leads = Blueprint("blueprint_leads", __name__, url_prefix = "/leads")

bp_leads.get("")(leads_controller.get_leads)
bp_leads.post("")(leads_controller.creat_lead)
bp_leads.patch("")(leads_controller.modify_lead)
bp_leads.delete("")(leads_controller.delete_lead)