from flask import Flask, render_template, request, url_for, redirect, session, flash, g

import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

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

#Route for signup
@app.route("/home")
def home():
    return render_template('home.html')

#Route for login
@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        db = get_db_connection()
        user = db.execute('SELECT user_id FROM Users WHERE email = ? AND password =?', (email, password)).fetchone()
        # return page. 
        if user: 
            session['logged_in'] = True
            session['user_id'] = user['user_id']
            return redirect(url_for('index'))
        else: 
            print('failed to login')
    if request.method == 'GET': 
        return render_template('login.html')

#Route for signup
@app.route("/signup")
def signup():
    return render_template('signup.html')

#Route for addEducation
@app.route("/addEducationData", methods=['GET','POST'])
def addEducationData():
 if request.method == 'POST':
       degree = request.form['degree']
       field_of_study = request.form['field_of_study']
       start_month = request.form['start_month']
       start_year  = request.form['start_year']
       end_month = request.form['end_month']
       end_year = request.form['end_year']
       grade = request.form['grade']
       
       db = get_db_connection()
       user = db.execute('INSERT INTO Education (degree, field_of_study, start_month, start_year, end_month, end_year, grade) VALUES (?, ?, ?, ?, ?, ?, ?)', (degree, field_of_study, start_month, start_year, end_month, end_year, grade))
       db.commit()

@app.route("/addEducation", methods=['GET','POST'])
def addEducation():
    addEducationData()
    return render_template('addEducation.html')

#Route for addExperience
@app.route("/addExperienceData", methods=['GET','POST'])
def addExperienceData():
 if request.method == 'POST':
    Title = request.form['Title']
    employmentType = request.form['employmentType']
    start_month = request.form['start_month']  
    start_year = request.form['start_year']
    end_month = request.form['end_month']
    end_year = request.form['end_year']
    industry = request.form['industry']

    db = get_db_connection()
    user = db.execute('INSERT INTO Experience (Title, employmentType, start_month, start_year, end_month, end_year, industry) VALUES (?, ?, ?, ?, ?, ?, ?)', (Title, employmentType, start_month, start_year, end_month, end_year, industry))
    db.commit()

@app.route("/addExperience", methods=['GET','POST'])
def addExperience():
    addExperienceData()
    return render_template('addExperience.html')

#Route for addCertification
@app.route("/addCertification")
def addCertification():
    return render_template('addCertification.html')

#Route for profile
@app.route("/profile")
def profile():
    return render_template('profile.html')

#Route for addSkill
@app.route("/addSkill")
def addSkill():
    return render_template('addSkill.html')

#Route for administrator
@app.route("/administrator")
def administrator():
    return render_template('administrator.html')

#Route for homepage
@app.route("/addhomepage")
def homepage():
    return render_template('homepage.html')