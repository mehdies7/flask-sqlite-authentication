from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
import sqlite3


class LoginForm(FlaskForm):
    username = StringField(
        "Username", render_kw={"placeholder": "username"}, validators=[DataRequired()]
    )
    password = PasswordField(
        "Password", render_kw={"placeholder": "username"}, validators=[DataRequired()]
    )
    submit = SubmitField("Login")

    def validate_username(self, username):
        conn = sqlite3.connect("database.db")
        curs = conn.cursor()
        curs.execute("SELECT username FROM users where username = (?)", [username.data])
        valusername = curs.fetchone()
        if valusername is None:
            raise ValidationError("This Username is not registered !!!")
