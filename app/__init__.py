from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # type: ignore

db = SQLAlchemy()

def create_app():
    # Create the Flask app instance
    app = Flask(__name__)

    # Configure the app with database settings and other configurations
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345678@localhost/user_provisioning'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking for performance
    app.secret_key = 'Akshat'  # Secret key for sessions (or encryption)

    # Initialize the database with the app
    db.init_app(app)

    # Import Blueprints after app is created to avoid circular imports
    from app.routes.user_routes import user_routes
    from app.routes.role_routes import role_routes
    from app.routes.assignment_routes import assignment_routes

    # Register the Blueprints with their respective URL prefixes
    app.register_blueprint(user_routes)
    app.register_blueprint(role_routes)
    app.register_blueprint(assignment_routes)

    return app
