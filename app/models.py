from datetime import datetime
from app import db  # Import the db instance from __init__.py

# Define the User model
class User(db.Model):
    __tablename__ = 'user'  # Optional: Custom table name in the database
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Primary key
    name = db.Column(db.String(100), nullable=False)  # Name column
    email = db.Column(db.String(100), unique=True, nullable=False)  # Unique email column
    status = db.Column(db.String(20), default='Active')  # User status
    created_date = db.Column(db.DateTime, default=datetime.utcnow)  # Auto-set timestamp

    # Relationship to UserRoleAssignment
    roles = db.relationship('UserRoleAssignment', backref='user', lazy=True)
    def to_dict(self):
        # Convert the User object into a dictionary
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'status': self.status,
            'created_date': self.created_date.strftime('%Y-%m-%d %H:%M:%S')  # Format the datetime field
        }
class Role(db.Model):
    __tablename__ = 'role'  # Optional: Custom table name
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Primary key
    name = db.Column(db.String(50), nullable=False)  # Role name
    description = db.Column(db.String(255))  # Role description

    # Relationship to UserRoleAssignment
    users = db.relationship('UserRoleAssignment', backref='role', lazy=True)
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }
class UserRoleAssignment(db.Model):
    __tablename__ = 'user_role_assignment'  # Optional: Custom table name
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Primary key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key to User
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)  # Foreign key to Role
    assigned_date = db.Column(db.DateTime, default=datetime.utcnow)
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "role_id": self.role_id,
            "assigned_date": self.assigned_date.strftime('%Y-%m-%d %H:%M:%S')
        }