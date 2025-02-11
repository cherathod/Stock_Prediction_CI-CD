from flask import Flask
from flask_login import LoginManager
from app.db import db
from app.config import Config
from app.routes.auth_routes import auth_bp
from app.routes.prediction_routes import prediction_bp
from app.routes.order_routes import order_bp
from app.routes.plot_routes import plot_bp

# Initialize Flask-Login
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # Load configuration settings
    app.config.from_object(Config)

    # Initialize the database
    db.init_app(app)

    # Initialize Flask-Login
    login_manager.init_app(app)

    # Set the login view (this ensures login_required redirects properly)
    login_manager.login_view = "auth.login"

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix="/")
    app.register_blueprint(prediction_bp, url_prefix="/", name="prediction_routes")
    app.register_blueprint(order_bp, url_prefix="/", name="order_routes")
    app.register_blueprint(plot_bp, url_prefix="/", name="plot_routes")

    return app

@login_manager.user_loader
def load_user(user_id):
    from app.models import RegisteredUser
    return RegisteredUser.query.get(int(id))  # Load user from DB
