#!/usr/bin/python3
"""
Flask app for Anti-Obesity App
"""

from flask import Flask, render_template

# Initialize the Flask application
app = Flask(__name__)

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

# Run the Flask application in debug mode
if __name__ == "__main__":
    app.run(debug=True)
