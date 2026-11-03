from flask import Blueprint

bp = Blueprint("anuncios", __name__)
from . import routes