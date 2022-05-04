import sqlite3
from flask import Flask, render_template, url_for, flash, request, redirect, Response
from dotenv import load_dotenv
from user import User
from flask_login import (
    LoginManager,
    UserMixin,
    login_required,
    login_user,
    logout_user,
    current_user,
)
from forms import LoginForm


load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = "FJAlYHv874eesSnnQPFMCvqekrkzEUQ3"

login_manager = LoginManager(app)
login_manager.login_view = "login"

# Database Connection
@login_manager.user_loader
def load_user(user_id):
    curs = get_database_connection()
    curs.execute("SELECT * from users where id = (?)", [user_id])
    lu = curs.fetchone()
    if lu is None:
        return None
    else:
        return User(int(lu[0]), lu[1], lu[2])


def get_database_connection():
    conn = sqlite3.connect("database.db")
    curs = conn.cursor()
    return curs


# the minimal Flask application
@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    flash("You have been logged out", "success")
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return render_template("index.html", title="Main Page")
    form = LoginForm()
    if form.validate_on_submit():
        curs = get_database_connection()

        curs.execute("SELECT * FROM users where username = (?)", [form.username.data])
        user = curs.fetchone()
        if user:
            Us = load_user(user[0])
            if form.password.data == Us.password:
                login_user(Us)
                return redirect(url_for("index"))
            else:
                flash("Incorrect Password", "danger")
        else:
            flash("Incorrect Username", "danger")

    return render_template("login.html", title="Login", form=form)


if __name__ == "__main__":
    app.run()
