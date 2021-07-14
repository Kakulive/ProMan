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
    return render_template('index.html')


@app.route("/get-boards")
@json_response
def get_boards():
    return queries.get_boards()


@app.route("/get-cards/<int:board_id>")
@json_response
def get_cards_for_board(board_id: int):
    return queries.get_cards_for_board(board_id)


@app.route("/get-columns/<int:board_id>")
@json_response
def get_columns_for_board(board_id: int):
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


@app.route("/create-new-card", methods=["POST"])
def create_new_card():
    data = request.get_json()
    board_id = int(data['board_id'])
    card_title = data['card_title']
    column_id = data['column_id']
    queries.save_card(board_id, card_title, column_id)


@app.route("/get-latest-card-id")
@json_response
def get_latest_card_id():
    return queries.get_latest_card_id()


@app.route("/get-first-column-from-board/<board_id>")
@json_response
def get_first_column_from_board(board_id):
    return queries.get_first_column_from_board(board_id)


@app.route("/delete-card/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    queries.delete_card(card_id)


@app.route("/update-card-title", methods=["PUT"])
def update_card_title():
    data = request.get_json()
    card_id = data['card_id']
    new_title_text = data['new_title_text']
    queries.update_card_title(card_id, new_title_text)


@app.route("/update-card-after-moving", methods=["PUT"])
def update_card_after_moving():
    data = request.get_json()
    card_id = data['card_id']
    column_id = data['column_id']
    card_order = data['card_order']
    queries.update_card_after_moving(card_id, column_id, card_order)


def main():
    app.run(
        debug=True
    )

    # Serving the favicon
    with app.app_context():
        app.add_url_rule('/favicon.ico', redirect_to=url_for('static', filename='favicon/favicon.ico'))


if __name__ == '__main__':
    main()
