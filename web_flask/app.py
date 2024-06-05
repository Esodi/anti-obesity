#!/usr/bin/python3
"""
Flask app for Anti-Obesity App
"""
from flask import Flask, render_template # type: ignore
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.Base_mode import db, User, Dietplan, Exerciseplan, Progress, Review # type: ignore
from models.user import user_bp # type: ignore
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:user@localhost/webappdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '800c6f1d3c90c0aac73d04823332d753a9bed56c141f4503205c107a9af71cde'

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(user_bp)

@app.route("/admin")
def admin():
    users = User.query.all()
    return render_template("admin.html", users=users)

# Define the route for the landing page
@app.route("/")
def index():
    return render_template("1-landing.html")

# Define the route for the explore page
@app.route("/explore")
def explore():
    return render_template("explore.html")

# Define the route for the register page
@app.route("/register")
def register():
    return render_template("register.html")

# Define the route for the login page
@app.route("/login")
def login():
    return render_template("login.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
