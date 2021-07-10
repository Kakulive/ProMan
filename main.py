from flask import Flask, render_template, url_for, flash, redirect, session, request
from util import json_response, hash_password
import queries as queries
import os
from datetime import timedelta


app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev')
app.permanent_session_lifetime = timedelta(days=1)


def login_required(function):
    def wrapper(*args, **kwargs):
        if 'username' not in session:
            flash("You must be logged in to do this!")
            return redirect(url_for('login'))
        return function(*args, **kwargs)
    wrapper.__name__ = function.__name__
    return wrapper


@app.route("/", methods=["GET", "POST"])
def index():
    """
    This is a one-pager which shows all the boards and cards
    """
    return render_template('index.html')


@app.route("/get-boards")
@json_response
def get_boards():
    """
    All the boards
    """
    return queries.get_boards()


@app.route("/get-cards/<int:board_id>")
@json_response
def get_cards_for_board(board_id: int):
    """
    All cards that belongs to a board
    :param board_id: id of the parent board
    """
    return queries.get_cards_for_board(board_id)


@app.route("/get-columns/<int:board_id>")
@json_response
def get_columns_for_board(board_id: int):
    """
    All cards that belongs to a board
    :param board_id: id of the parent board
    """
    return queries.get_columns_for_board(board_id)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = hash_password(password)
        queries.save_user(username, email, hashed_password)
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        if queries.check_user_login(email, password):
            session['email'] = email
            session['username'] = queries.get_user_username(email)
            flash(f"You were successfully logged in, {session['username']}")
        else:
            flash('Login failed. Try again!')

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))


def main():
    app.run(
        debug=True
    )

    # Serving the favicon
    with app.app_context():
        app.add_url_rule('/favicon.ico', redirect_to=url_for('static', filename='favicon/favicon.ico'))


if __name__ == '__main__':
    main()
