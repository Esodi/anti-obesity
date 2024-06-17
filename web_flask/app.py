#!/usr/bin/python3
"""
Flask app for Anti-Obesity App
"""
from flask import Flask, render_template, request # type: ignore
from flask_migrate import Migrate
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.Base_mode import db, User, Dietplan, Exerciseplan, Progress, Review # type: ignore
from models.user import user_bp # type: ignore
from models.diet_plan import dietplan_bp # type: ignore
from make_celery import make_celery
from tasks import send_exercise_reminders

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:user@localhost/webappdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '800c6f1d3c90c0aac73d04823332d753a9bed56c141f4503205c107a9af71cde'

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(user_bp)
app.register_blueprint(dietplan_bp, url_prefix='/')

app.config.from_object('config')
celery = make_celery(app)

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(300.0, send_exercise_reminders.s(), name='send exercise reminders every 5 minutes')

@app.route("/admin")
def admin():
    users = User.query.all()
    return render_template("admin.html", users=users)

# Define the route for the landing page
@app.route("/")
def index():
    return render_template("landing.html")

# Define the route for the explore page
@app.route("/explore")
def explore():
    return render_template("explore.html")

# Define the route for the explore page
@app.route("/dashboard")
def dash_board():
    return render_template("user_dashboard.html")

# Define the route for the login page
@app.route("/login")
def login():
    return render_template("login.html")

@app.route('/calculate', methods=['POST', 'GET'])
def calculate():
    if request.method == 'POST':
        weight = float(request.form['weight'])
        height = float(request.form['height'])

        # Calculate BMI
        bmi = round((weight / (height ** 2)), 2)

        # Determine BMI category
        if bmi < 18.5:
            category = 'Underweight'
        elif bmi < 24.9:
            category = 'Normal weight'
        elif bmi < 29.9:
            category = 'Overweight'
        else:
            category = 'Obese'

        return render_template('result.html', bmi=bmi, category=category)

    return render_template('bmi.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
