<<<<<<< Updated upstream
from flask import Flask, render_template, request, url_for, redirect, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key="__privatekey__"
=======
from flask import Flask, render_template, request, url_for, redirect, session, flash, g

import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'
>>>>>>> Stashed changes

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
@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        print('am i here')
        email = request.form['email']
        password = request.form['password']

        db = get_db_connection()
        user = db.execute('SELECT user_id FROM Users WHERE email = ? AND password_hash =?', (email, password)).fetchone()
        # return page. 
        if user: 
            session['logged_in'] = True
            session['user_id'] = user['user_id']
            print(session['user_id'])
            return redirect(url_for('index'))
        else: 
            print('failed to login')
    if request.method == 'GET': 
        print('i am in get method')
        return render_template('login.html')

#Route for signup
@app.route("/signup", methods=['POST', 'GET'])
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

#Route for profile
@app.route("/profile")
def profile():
    return render_template('profile.html')

@app.route("/addSkill")
def addSkill():
    return render_template('addSkill.html')
