#!/bin/python3
""" represent user class """

from flask import Blueprint, request, render_template, redirect, url_for, flash, session # type: ignore
from models.Base_mode import db, User # type: ignore

user_bp = Blueprint('user', __name__)


@user_bp.route('/users/new', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        age = request.form['age']
        password = request.form['password']
        
        new_user = User(username=username, email=email, age=age)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('User created successfully')
        return redirect(url_for('user.create_user'))
    
    return render_template('create_user.html')


@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return render_template('user_detail.html', user=user)
    else:
        return "User not found", 404


@user_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        flash('User not found')
        return redirect(url_for('user.create_user'))
    
    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        user.age = request.form['age']
        if 'password' in request.form and request.form['password']:
            user.set_password(request.form['password'])
        
        db.session.commit()
        flash('User updated successfully')
        return redirect(url_for('user.get_user', user_id=user_id))
    
    return render_template('edit_user.html', user=user)


@user_bp.route('/delusers/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return redirect('/')
    else:
        return "User not found", 404


@user_bp.route('/edit_user/<int:user_id>', methods=['GET'])
def edit_user(user_id):
    user = User.query.get(user_id)
    return render_template('edit_user.html', user=user)


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            flash('Login successful')
            return redirect(url_for('user.get_user', user_id=user.id))
        else:
            flash('Invalid email or password')
    return render_template('login.html')

@user_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully')
    return redirect(url_for('user.login'))