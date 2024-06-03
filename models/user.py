#!/bin/python3
""" represent user class """

# user_routes.py
from flask import Blueprint, request, render_template, redirect # type: ignore
from models.Base_mode import db, User # type: ignore

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['POST'])
def create_user():
    username = request.form['username']
    email = request.form['email']
    age = request.form['age']
    password_hash = request.form['password_hash']

    new_user = User(username=username, email=email, age=age, password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/')

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return render_template('user_detail.html', user=user)
    else:
        return "User not found", 404

@user_bp.route('/users/<int:user_id>', methods=['POST'])
def update_user(user_id):
    user = User.query.get(user_id)
    if user:
        user.username = request.form['username']
        user.email = request.form['email']
        user.age = request.form['age']
        user.password_hash = request.form['password_hash']
        
        db.session.commit()
        return redirect(f'/users/{user_id}')
    else:
        return "User not found", 404

@user_bp.route('/delusers/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return redirect('/')
    else:
        return "User not found", 404

@user_bp.route('/new_user', methods=['GET'])
def new_user():
    return render_template('user.html')

@user_bp.route('/edit_user/<int:user_id>', methods=['GET'])
def edit_user(user_id):
    user = User.query.get(user_id)
    return render_template('edit_user.html', user=user)