import os
import secrets
import connexion
from flask import Flask
from extensions import db

def create_app():
    connex_app = connexion.App(__name__, specification_dir="static/")
    app = connex_app.app

    # Set a securely generated secret key
    app.secret_key = secrets.token_hex(32)

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    db_path = os.path.join(app.instance_path, "Authors.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    # Import models so they are registered with SQLAlchemy
    import models
    with app.app_context():
        db.create_all()

    # Import handlers after app and db are ready
    import handlers.home
    import handlers.authors
    import handlers.books
    import handlers.reviews

    connex_app.add_api("app.yaml")
    return connex_app

if __name__ == "__main__":
    app = create_app()
    app.run(port=5050, debug=True)
