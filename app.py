from flask import Flask, render_template, request, url_for, redirect, session, flash, g
import sqlite3

app = Flask(__name__)

#DB Connection Function Object
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

#Routes
@app.route("/")
def index():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM Users').fetchall()
    conn.close()  
    return render_template('index.html', users=users)

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

@app.route("/addSkill")
def addSkill():
    return render_template('addSkill.html')
