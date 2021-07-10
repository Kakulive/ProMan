import bcrypt
import data_manager
import util


def get_card_status(status_id):
    """
    Find the first status matching the given id
    :param status_id:
    :return: str
    """
    status = data_manager.execute_select(
        """
        SELECT * FROM statuses s
        WHERE s.id = %(status_id)s
        ;
        """, {"status_id": status_id})

    return status


def get_boards():
    """
    Gather all boards
    :return:
    """
    return data_manager.execute_select(
        """
        SELECT * FROM boards
        ORDER BY id DESC
        ;
        """
    )


def get_cards_for_board(board_id):
    matching_cards = data_manager.execute_select(
        """
        SELECT * FROM cards
        WHERE cards.board_id = %(board_id)s
        ;
        """, {"board_id": board_id})

    return matching_cards


def get_columns_for_board(board_id):
    matching_columns = data_manager.execute_select(
        """
        SELECT columns.id, statuses.status
        FROM columns
        JOIN statuses
        ON columns.status_id = statuses.id
        WHERE columns.board_id = %(board_id)s
        ;
        """, {"board_id": board_id})

    return matching_columns


def save_user(username, email, hashed_password):
    registration_time = str(util.get_current_time())
    data_manager.execute_update(
        """
        INSERT INTO users
        (username, password, email, submission_time)
        VALUES 
        (%(username)s, %(password)s, %(email)s, %(submission_time)s)
        ;
        """, {"username": username, "password": hashed_password, "email": email, "submission_time": registration_time})


def check_user_login(email, password):
    user_password = data_manager.execute_select(
        """
        SELECT password
        FROM users
        WHERE email = %(email)s
        ;
        """, {"email": email})

    return bcrypt.checkpw(password.encode('UTF-8'), user_password[0]['password'].encode('UTF-8'))


def get_user_username(email):
    user_username = data_manager.execute_select(
        """
        SELECT username
        FROM users
        WHERE email = %(email)s
        ;
        """, {"email": email})

    return user_username[0]['username']
