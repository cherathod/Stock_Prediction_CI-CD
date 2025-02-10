from flask import Blueprint

# Create a Blueprint for routes
main_bp = Blueprint("main", __name__)

def register_routes(app):
    from .auth_routes import auth_bp
    from .order_routes import order_bp
    from .plot_routes import plot_bp
    from .prediction_routes import prediction_bp

    # Register Blueprints only if not already registered
    if "order_bp" not in app.blueprints:
        app.register_blueprint(order_bp, url_prefix="/orders")

    if "plot_bp" not in app.blueprints:
        app.register_blueprint(plot_bp, url_prefix="/plots")

    if "prediction_bp" not in app.blueprints:
        app.register_blueprint(prediction_bp, url_prefix="/predict")