from flask import Flask, render_template, request, url_for, redirect, session, flash

app = Flask(__name__)

@app.route("/")
def index():
    return "index"

@app.route("/login")
def login():
    return render_template('login.html')