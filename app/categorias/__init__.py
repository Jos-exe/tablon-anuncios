from flask import Blueprint

bp = Blueprint("categorias", __name__, url_prefix="/categorias")
from . import routes