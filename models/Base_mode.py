#!/bin/python3
"""
Base model for anti-Obesity web app
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    dietplans = db.relationship('Dietplan', backref='user', lazy=True)
    exerciseplans = db.relationship('Exerciseplan', backref='user', lazy=True)
    progress = db.relationship('Progress', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)


class Dietplan(db.Model):
    __tablename__ = 'dietplans'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class Exerciseplan(db.Model):
    __tablename__ = 'exerciseplans'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class Progress(db.Model):
    __tablename__ = 'progresses'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    body_fat_percentage = db.Column(db.Float, nullable=True)
    muscle_mass = db.Column(db.Float, nullable=True)
    entry_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())


class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
