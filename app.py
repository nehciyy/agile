from flask import Flask, render_template, request, url_for, redirect, session, flash

app = Flask(__name__)

@app.route("/")
def index():
    return "index"

#Route for login
@app.route("/login")
def login():
    return render_template('login.html')

#Route for signup
@app.route("/signup")
def signup():
    return render_template('signup.html')

#Route for addEducation
@app.route("/addEducation")
def addEducation():
    return render_template('addEducation.html')

#Route for addExperience
@app.route("/addExperience")
def addExpereience():
    return render_template('addExperience.html')

#Route for addCertification
@app.route("/addCertification")
def addExpereience():
    return render_template('addCertification.html')

#Route for profile
@app.route("/profile")
def profile():
    return render_template('profile.html')