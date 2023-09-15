from flask import Flask, render_template, request, url_for, redirect, session, flash, g
from flask_tinymce import TinyMCE

import sqlite3
import recommendation as jobalgorithm
import os.path


app = Flask(__name__)
app.secret_key = "your_secret_key"
tinymce = TinyMCE()
tinymce.init_app(app)


# DB Connection Function Object
def get_db_connection():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "database.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


# Checks if User is authenticated.
def authenticated():
    if "user_id" in session:
        # User is authenticated, allow access
        return True
    else:
        # User is not authenticated, return False
        return False


# Checks if user is an admin
def is_admin():
    if "user_id" in session:
        user_id = session["user_id"]
        conn = get_db_connection()
        query = "SELECT is_admin FROM Users WHERE user_id = ?"
        is_admin = conn.execute(query, (user_id,)).fetchone()[0]
        conn.close()
        if is_admin == "True":
            return True
        else:
            return False
    else:
        return False


# Routes
@app.route("/")
def index():
    return render_template("login.html")


# Route for login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = get_db_connection()
        user = db.execute(
            "SELECT user_id FROM Users WHERE email = ? AND password =?",
            (email, password),
        ).fetchone()
        # return page.
        if user:
            session["logged_in"] = True
            session["user_id"] = user[0]
            if is_admin():
                return redirect(url_for("administrator"))
            else:
                return redirect(url_for("home"))
        else:
            flash("Invalid email or password. Please try again.")

    if request.method == "GET":
        return render_template("login.html")

    # Ensure the route returns a valid response even if the login fails
    return render_template("login.html")


# Route for logout
@app.route("/logout")
def logout():
    # Remove the 'user_id' key from the session
    session.pop("user_id", None)
    # Redirect the user to the login page or any other desired destination
    return redirect(url_for("login"))


# Route for signup
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        email = request.form["email"]
        dateofbirth = request.form["date_of_birth"]
        gender = request.form["gender"]
        password = request.form["password"]
        confirmpassword = request.form["confirmpassword"]

        if password == confirmpassword:
            db = get_db_connection()
            # Insert into User Table
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO Users (email, password) VALUES (?, ?)", (email, password)
            )
            db.commit()
            # Get the user_id of the inserted user
            user_id = cursor.lastrowid
            # Insert into Accounts Table
            cursor.execute(
                "INSERT INTO Accounts (userid, First_name, Last_name, date_of_birth, gender) VALUES (?, ?, ?, ?, ?)",
                (user_id, firstname, lastname, dateofbirth, gender),
            )
            db.commit()
            user_id = cursor.lastrowid
            # Add the user_id to the session
            session["logged_in"] = True
            session["user_id"] = user_id
            print(session["user_id"])
            # Close the cursor and database connection
            cursor.close()
            db.close()
            return redirect(url_for("addSkill"))
        else:
            print("Password or confirm password is not filled")
            return redirect(url_for("signup"))
    if request.method == "GET":
        return render_template("signup.html")


# Route for addEducation
@app.route("/addEducation", methods=["GET", "POST"])
def addEducation():
    if authenticated():
        if request.method == "POST":
            account_id = session["user_id"]
            degree = request.form["degree"]
            field_of_study = request.form["field_of_study"]
            start_month = request.form["start_month"]
            start_year = request.form["start_year"]
            end_month = request.form["end_month"]
            end_year = request.form["end_year"]
            grade = request.form["grade"]

            db = get_db_connection()
            user = db.execute(
                "INSERT INTO Education (account_id, degree, field_of_study, start_month, start_year, end_month, end_year, grade) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    account_id,
                    degree,
                    field_of_study,
                    start_month,
                    start_year,
                    end_month,
                    end_year,
                    grade,
                ),
            )
            db.commit()
            return redirect(url_for("profile"))

        if request.method == "GET":
            about = about_content()
            return render_template("addEducation1.html", about=about, admin=is_admin())
    else:
        # User is not authenticated, redirect them to the login page or perform other actions
        return redirect(url_for("login"))


# Route for addExperience
@app.route("/addExperience", methods=["GET", "POST"])
def addExperience():
    if authenticated():
        if request.method == "POST":
            account_id = session["user_id"]
            Title = request.form["Title"]
            employmentType = request.form["employmentType"]
            start_month = request.form["start_month"]
            start_year = request.form["start_year"]
            end_month = request.form["end_month"]
            end_year = request.form["end_year"]
            description = request.form["tinymce"]

            db = get_db_connection()
            user = db.execute(
                "INSERT INTO Experience (account_id, Title, employmentType, start_month, start_year, end_month, end_year, role_description) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    account_id,
                    Title,
                    employmentType,
                    start_month,
                    start_year,
                    end_month,
                    end_year,
                    description,
                ),
            )
            db.commit()
            return redirect(url_for("addEducation"))

        if request.method == "GET":
            about = about_content()
            return render_template("addExperience.html", about=about, admin=is_admin())
    else:
        # User is not authenticated, redirect them to the login page or perform other actions
        return redirect(url_for("login"))


# Route for profile
@app.route("/profile")
def profile():
    if authenticated():
        about = about_content()
        education = education_content()
        experience = experience_content()
        skills = skills_content()
        admin = is_admin()
        return render_template(
            "profile.html",
            about=about,
            skills=skills,
            education=education,
            experience=experience,
            admin=admin,
        )
    else:
        # User is not authenticated, redirect them to the login page or perform other actions
        return redirect(url_for("login"))


def about_content():
    db = get_db_connection()
    account_id = session["user_id"]
    query = "SELECT A.First_name, A.Last_name, A.date_of_birth, A.gender, U.email FROM Accounts A JOIN Users U ON A.userid = U.user_id WHERE A.userid = ?"
    user = db.execute(query, (account_id,)).fetchall()
    db.close()
    return user


def skills_content():
    db = get_db_connection()
    account_id = session["user_id"]
    skills = db.execute(
        "SELECT skills, proficiency FROM Skills WHERE account_id = ?", (account_id,)
    ).fetchall()
    db.close()
    return skills


def education_content():
    db = get_db_connection()
    account_id = session["user_id"]
    education = db.execute(
        "SELECT degree, field_of_study, start_month, start_year, end_month, end_year, grade FROM Education WHERE account_id = ?",
        (account_id,),
    ).fetchall()
    db.close()
    return education


def experience_content():
    db = get_db_connection()
    account_id = session["user_id"]
    experience = db.execute(
        "SELECT Title, employmentType, start_month, start_year, end_month, end_year, role_description FROM Experience WHERE account_id = ?",
        (account_id,),
    ).fetchall()
    db.close()
    return experience


@app.route("/editprofile", methods=["POST"])
def edit_profile():
    if authenticated():
        if request.method == "POST":
            account_id = session["user_id"]
            email = request.form["email"]
            DOB = request.form["date_of_birth"]
            gender = request.form["gender"]

            try:
                db = get_db_connection()
                cursor = db.cursor()
                cursor.execute("BEGIN TRANSACTION;")
                cursor.execute(
                    "UPDATE Users SET email = ? WHERE user_id = ?",
                    (
                        email,
                        account_id,
                    ),
                )
                cursor.execute(
                    "UPDATE Accounts SET date_of_birth = ?, gender = ? WHERE userid = ?",
                    (
                        DOB,
                        gender,
                        account_id,
                    ),
                )
                cursor.execute("COMMIT;")
            except Exception as e:
                flash("An error occurred while deleting the account and related data.")
            finally:
                db.close()

            return redirect(url_for("profile"))
    else:
        return redirect(url_for("login"))


# Route for addSkill
@app.route("/addSkill", methods=["GET", "POST"])
def addSkill():
    if authenticated():
        if request.method == "POST":
            skills = request.form.getlist("skills[]")
            proficiencies = request.form.getlist("proficiency[]")
            account_id = session["user_id"]

            for i in range(len(skills)):
                skills[i] = skills[i].lower()

            for skill, proficiency in zip(skills, proficiencies):
                db = get_db_connection()
                user = db.execute(
                    "INSERT INTO Skills (account_id, skills, proficiency) VALUES (?,?,?)",
                    (account_id, skill, proficiency),
                )
                db.commit()
            return redirect(url_for("addSkill"))

        if request.method == "GET":
            conn = get_db_connection()
            about = about_content()
            account_id = session["user_id"]
            print(account_id)
            skills = conn.execute(
                "SELECT skill_id, skills, proficiency FROM Skills WHERE account_id = ?",
                (account_id,),
            ).fetchall()
            conn.close()
            return render_template(
                "addSkill.html", skills=skills, about=about, admin=is_admin()
            )
    else:
        # User is not authenticated, redirect them to the login page or perform other actions
        return redirect(url_for("login"))


# Route to delete skill
@app.route("/deleteSkill", methods=["POST"])
def delete_skill():
    if authenticated():
        try:
            db = get_db_connection()
            cursor = db.cursor()
            account_id = session["user_id"]
            skill_id = request.form.get("skill_id")
            print("Skill_id: " + skill_id)
            cursor.execute(
                "DELETE FROM Skills WHERE account_id = ? AND skill_id = ?",
                (account_id, skill_id),
            )
            db.commit()
        except sqlite3.Error as e:
            print("Error:", e)
        finally:
            db.close()

        return redirect(url_for("addSkill"))
    else:
        # User is not authenticated, redirect them to the login page or perform other actions
        return redirect(url_for("login"))


# Route for administrator
@app.route("/administrator", methods=["GET"])
def administrator():
    if is_admin():
        conn = get_db_connection()
        query = "SELECT A.account_id, A.First_name, A.Last_name, U.email FROM Accounts A JOIN Users U ON A.userid = U.user_id WHERE is_admin = 'False'"
        user = conn.execute(query).fetchall()
        conn.close()
        return render_template(
            "administrator.html", accounts=user, admin=is_admin(), about=about
        )
    else:
        # User is not authenticated, redirect them to the login page or perform other actions
        return redirect(url_for("error"))


# Route to delete account for administrator
@app.route("/deleteAccount", methods=["POST"])
def delete_account():
    if authenticated():
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            # Retrieve account_id from the form data
            account_id = request.form.get("account_id")
            print(account_id)
            # Execute the DELETE queries within a transaction
            cursor.execute("BEGIN TRANSACTION;")
            # Delete from Education table
            cursor.execute("DELETE FROM Education WHERE account_id = ?", (account_id,))
            # Delete from Experience table
            cursor.execute("DELETE FROM Experience WHERE account_id = ?", (account_id,))
            # Delete from Skills table
            cursor.execute("DELETE FROM Skills WHERE account_id = ?", (account_id,))
            # Delete from Users table
            cursor.execute(
                "DELETE FROM Users WHERE user_id = (SELECT userid FROM Accounts WHERE account_id = ?)",
                (account_id,),
            )
            # Delete from Accounts table
            cursor.execute("DELETE FROM Accounts WHERE account_id = ?", (account_id,))
            # Commit the transaction
            cursor.execute("COMMIT;")
            flash(
                "All data related to the account has been deleted successfully!",
                "success",
            )

        except Exception as e:
            flash(
                "An error occurred while deleting the account and related data.",
                "error",
            )

        finally:
            conn.close()

        return redirect(url_for("administrator"))
    else:
        # User is not authenticated, redirect them to the login page or perform other actions
        return redirect(url_for("login"))


# Route for index
@app.route("/home", methods=["GET", "POST"])
def home():
    if authenticated():
        about = about_content()
        admin = is_admin()
        if request.method == "GET":
            conn = get_db_connection()
            cursor = conn.cursor()

            # Use a parameterized query to delete rows
            query_delete = """
                DELETE FROM recommendateJobs
                WHERE account_id IN (
                    SELECT account_id
                    FROM Accounts
                    WHERE userid = ?
                )
            """
            try:
                cursor.execute(query_delete, (session["user_id"],))
                conn.commit()
                print("Rows deleted successfully.")
            except sqlite3.Error as e:
                print("Error:", e)
            # After deletion, retrieve updated recommendations
            jobalgorithm.main(session["user_id"])

            # Query for recommendations after deletion
            query_select = """
                        SELECT R.* 
                        FROM recommendateJobs AS R
                        JOIN Accounts AS A ON R.account_id = A.account_id
                        WHERE A.userid = ? AND R.match <> 0.0
                        ORDER BY R.match DESC
                    """
            cursor.execute(query_select, (session["user_id"],))
            results = cursor.fetchall()

            conn.close()
            return render_template(
                "index.html", recommendations=results, about=about, admin=admin
            )
    else:
        # User is not authenticated, redirect them to the login page or perform other actions
        return redirect(url_for("login"))


# Route for Error
@app.route("/error", methods=["GET"])
def error():
    if authenticated():
        return render_template("errorMessage.html")
    else:
        return redirect(url_for("login"))
