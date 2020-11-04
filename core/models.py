import uuid
from core import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    # id = db.Column('id', db.Text(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    permit = db.relationship('Permit', backref='author', lazy=True)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"{self.email} of {self.username}"

    def is_active(self):
        return True


class Permit(db.Model):

    __tablename__ = 'permit'

    # id = db.Column('id', db.Text(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    mileage = db.Column(db.Numeric(), nullable=False)
    text = db.Column(db.Text, nullable=False)
    resolved = db.Column(db.String(100), default=False, nullable=False)
    follow_up = db.Column(db.String(100), default=False, nullable=False)

    users = db.relationship(User)

    def __init__(self, user_id, title, text, location, mileage, resolved, follow_up):

        self.user_id = user_id
        self.title = title
        self.text = text
        self.location = location
        self.mileage = mileage
        self.resolved = resolved
        self.follow_up = follow_up

    def __repr__(self):
        return f"{self.title}, ID {self.id} by {self.date} to {self.location}"

