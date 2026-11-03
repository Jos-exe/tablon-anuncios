from flask import Flask
from config import Config
from .extensions import db, migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)

    from . import models
    from .auth import bp as auth_bp
    from .anuncios import bp as anuncios_bp
    from .usuarios import bp as usuarios_bp
    from .categorias import bp as categorias_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(anuncios_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(categorias_bp)
    return app