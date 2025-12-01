import os
from flask import Flask
from config import Config
from database import db
from models import User
from werkzeug.security import generate_password_hash
from flask_login import LoginManager

def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(Config)

    # Ensure uploads folder exists
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Initialize extensions
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    # Import blueprints
    from auth import auth_bp
    from main import main_bp
    from seller import seller_bp
    from admin import admin_bp

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(seller_bp)
    app.register_blueprint(admin_bp)

    # Flask 3.0: create tables immediately when app starts
    with app.app_context():
        db.create_all()
        create_default_admin()

    # Login loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app


def create_default_admin():
    admin_username = os.getenv("QC_ADMIN_USER", "admin")
    admin_pass = os.getenv("QC_ADMIN_PASS", "adminpass")

    admin = User.query.filter_by(username=admin_username).first()

    if admin is None:
        new_admin = User(
            username=admin_username,
            is_admin=True
        )
        new_admin.set_password(admin_pass)
        db.session.add(new_admin)
        db.session.commit()

        print(f"[INFO] Default admin created → user: {admin_username}, password: {admin_pass}")
    else:
        print("[INFO] Admin already exists — no new admin created.")


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
