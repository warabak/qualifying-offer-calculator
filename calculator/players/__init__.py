from flask import Blueprint

api_bp = Blueprint("api_bp", __name__, url_prefix="/")

from calculator.players import players
