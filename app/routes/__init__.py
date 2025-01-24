from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345678@localhost/user_provisioning'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'Akshat'

    db.init_app(app)

    # Import and register Blueprints
    from app.routes.user_routes import user_routes
    from app.routes.role_routes import role_routes
    from app.routes.assignment_routes import assignment_routes

    app.register_blueprint(user_routes, url_prefix='/api/users')
    app.register_blueprint(role_routes, url_prefix='/api/roles')
    app.register_blueprint(assignment_routes, url_prefix='/api/assignments')

    return app