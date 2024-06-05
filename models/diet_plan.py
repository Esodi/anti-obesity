# dietplan_routes.py
from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from models.Base_mode import db, Dietplan, User
from functools import wraps

dietplan_bp = Blueprint('dietplan', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('user.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@dietplan_bp.route('/dietplans/new', methods=['GET', 'POST'])
@login_required
def create_dietplan():
    if request.method == 'POST':
        user_id = session['user_id']
        name = request.form['name']
        description = request.form['description']
        calories_per_day = request.form['calories_per_day']
        
        new_dietplan = Dietplan(
            user_id=user_id,
            name=name,
            description=description,
            calories_per_day=calories_per_day
        )
        db.session.add(new_dietplan)
        db.session.commit()
        
        flash('Diet plan created successfully')
        return redirect(url_for('dietplan.list_dietplans'))
    
    return render_template('create_dietplan.html')

@dietplan_bp.route('/dietplans')
@login_required
def list_dietplans():
    user_id = session['user_id']
    dietplans = Dietplan.query.filter_by(user_id=user_id).all()
    return render_template('list_dietplans.html', dietplans=dietplans)

@dietplan_bp.route('/dietplans/<int:dietplan_id>')
@login_required
def view_dietplan(dietplan_id):
    dietplan = Dietplan.query.get_or_404(dietplan_id)
    if dietplan.user_id != session['user_id']:
        flash('You do not have permission to view this diet plan')
        return redirect(url_for('dietplan.list_dietplans'))
    return render_template('view_dietplan.html', dietplan=dietplan)

@dietplan_bp.route('/dietplans/<int:dietplan_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_dietplan(dietplan_id):
    dietplan = Dietplan.query.get_or_404(dietplan_id)
    if dietplan.user_id != session['user_id']:
        flash('You do not have permission to edit this diet plan')
        return redirect(url_for('dietplan.list_dietplans'))

    if request.method == 'POST':
        dietplan.name = request.form['name']
        dietplan.description = request.form['description']
        dietplan.calories_per_day = request.form['calories_per_day']
        db.session.commit()
        
        flash('Diet plan updated successfully')
        return redirect(url_for('dietplan.view_dietplan', dietplan_id=dietplan_id))
    
    return render_template('edit_dietplan.html', dietplan=dietplan)
