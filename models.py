from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False) # 'admin' or 'faculty'

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time_slot = db.Column(db.String(50), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'))
    subject = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(10), default="#3498db")

    room = db.relationship('Room', backref='schedules')
    faculty = db.relationship('Faculty', backref='schedules')