from flask import Blueprint

bp = Blueprint("usuarios", __name__)
from . import routes