from . import db
from flask_login import UserMixin
from datetime import datetime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    projects = db.relationship('Project', backref='user', lazy=True)



class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(140))
    name = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    value = db.Column(db.Integer, nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    client = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tasks = db.relationship('Task', backref='task', lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
        return '<Project {}>'.format(self.name)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    description = db.Column(db.Text)
    genre = db.Column(db.String(50))
    duration = db.Column(db.Integer)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    project_id = db.Column(
        db.Integer, db.ForeignKey('project.id'), nullable=False)

    def __repr__(self):
        return '<Task {}>'.format(self.title)

