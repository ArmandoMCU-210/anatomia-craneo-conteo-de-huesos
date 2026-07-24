import os

from flask import Flask

from config import Config

from .extensions import db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    if not os.environ.get("VERCEL"):
        # En Vercel el proyecto es de solo lectura (salvo /tmp); solo creamos la
        # carpeta instance/ para el SQLite local en desarrollo.
        instance_dir = os.path.join(os.path.dirname(app.root_path), "instance")
        os.makedirs(instance_dir, exist_ok=True)

    db.init_app(app)

    from .blueprints.main.routes import main_bp
    from .blueprints.game.routes import game_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(game_bp)

    with app.app_context():
        db.create_all()

    return app
