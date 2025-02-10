from flask import Flask
from app.db import db  # Import db from the db module
from app.config import Config  # Import config to use configuration settings
from app.routes.auth_routes import auth_bp  # authentication routes
from app.routes.prediction_routes import prediction_bp  # prediction routes
from app.routes.order_routes import order_bp  # order routes
from app.routes.plot_routes import plot_bp  #  plot routes
from app.routes.dashboard_routes import dashboard_bp  # dashboard routes

def create_app():
    app = Flask(__name__)

    # Load configuration settings from the Config class
    app.config.from_object(Config)

    # Initialize the db with the app
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(prediction_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(plot_bp)
    app.register_blueprint(dashboard_bp)
    

    return app
