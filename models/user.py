from app import db, UserFollow
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    
    # Add the following fields
    bio = db.Column(db.Text)
    profile_picture = db.Column(db.String(255))  # You might want to store the file path or use Flask-Uploads

    # Relationships
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    likes = db.relationship('PostLike', backref='user', lazy='dynamic')
    followers = db.relationship('UserFollow', foreign_keys=[UserFollow.following_id], backref='following', lazy='dynamic')
    following = db.relationship('UserFollow', foreign_keys=[UserFollow.follower_id], backref='follower', lazy='dynamic')

    # Methods for password hashing
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
