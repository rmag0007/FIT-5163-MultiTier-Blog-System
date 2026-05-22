from extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email_encrypted = db.Column(db.Text, nullable=False)   # Encrypted PII
    password_hash = db.Column(db.String(200), nullable=False)
    tier = db.Column(db.String(20), nullable=False, default="basic")  # "basic" | "premium"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ActivityLog(db.Model):
    __tablename__ = "activity_logs"

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    session_id = db.Column(db.String(100))          # Anonymous reader session
    event_type = db.Column(db.String(50))           # "view", "comment", "share", "like"
    time_spent_seconds = db.Column(db.Integer, default=0)
    scroll_depth_percent = db.Column(db.Integer, default=0)
    ip_encrypted = db.Column(db.Text)               # Encrypted PII
    country = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)