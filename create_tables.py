from app import create_app, db  # Import create_app and db
from app.models import User, Role, UserRoleAssignment  # Import your models

# Create the app instance
app = create_app()
# Use the app context to ensure proper database access
with app.app_context():
    db.create_all()  # This will create the tables in your MySQL database
    print("Tables created successfully!")