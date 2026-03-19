import os
from flask import Flask
from extensions import db, migrate


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mommyscanner.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change-me-in-production")

    db.init_app(app)
    migrate.init_app(app, db)

    import models  # noqa: F401 – ensure models are registered with SQLAlchemy
    from routes import register_routes
    register_routes(app)

    return app


app = create_app()

if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=5000, debug=debug)
