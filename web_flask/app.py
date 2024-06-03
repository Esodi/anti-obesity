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

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:user@localhost/webappdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.register_blueprint(user_bp)

@app.route("/")
def index():
    users = User.query.all()
    return render_template("index.html", users=users)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
