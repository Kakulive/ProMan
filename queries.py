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
        ORDER BY card_order;
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
        ORDER BY column_order;
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


def get_first_column_from_board(board_id):
    user_username = data_manager.execute_select(
        """
        SELECT id
        FROM columns
        WHERE board_id = %(board_id)s
        ORDER BY column_order
        LIMIT 1
        ;
        """, {"board_id": board_id})

    return user_username[0]['id']


def get_latest_card_id():
    return data_manager.execute_select(
        """
        SELECT max(id)
        FROM cards;
        """
    )[0]['max']


def get_latest_column_id():
    return data_manager.execute_select(
        """
        SELECT max(id)
        FROM columns;
        """
    )[0]['max']


def save_card(board_id, card_title, column_id):
    max_card_order = data_manager.execute_select(
        """
        SELECT MAX(card_order)
        FROM cards
        WHERE board_id = %(board_id)s and column_id = %(column_id)s;
        """, {"board_id": board_id, "column_id": column_id})[0]['max']
    max_card_order += 1

    status_id = data_manager.execute_select(
        """
        SELECT status_id
        FROM cards
        WHERE board_id = %(board_id)s and column_id = %(column_id)s
        LIMIT 1;
        """, {"board_id": board_id, "column_id": column_id})[0]['status_id']

    data_manager.execute_update(
        """
        INSERT INTO cards 
        (board_id, status_id, title, card_order, column_id)
        VALUES 
        (%(board_id)s, %(status_id)s, %(title)s, %(card_order)s, %(column_id)s); 
        """, {"board_id": int(board_id), "status_id": status_id, "title": card_title,
              "card_order": max_card_order, "column_id": int(column_id)})


def create_new_column(board_id, status_id, column_order):
    data_manager.execute_update(
        """
        INSERT INTO columns 
        (board_id, status_id, column_order)
        VALUES 
        (%(board_id)s, %(status_id)s, %(column_order)s); 
        """, {"board_id": board_id, "status_id": status_id, "column_order": column_order})


def delete_card(card_id):
    data_manager.execute_update(
        """
        DELETE from cards
        WHERE id = %(card_id)s;
        """, {"card_id": card_id})


def update_card_title(card_id, new_title_text):
    data_manager.execute_update(
        """
        UPDATE cards
        SET title = %(new_title_text)s
        WHERE id = %(card_id)s;
        """, {"card_id": card_id, "new_title_text": new_title_text})


def update_card_after_moving(card_id, column_id, card_order):
    data_manager.execute_update(
        """
        UPDATE cards
        SET card_order = card_order + 1
        WHERE card_order >= %(card_order)s AND column_id=%(column_id)s;
        """, {"card_order": card_order, "column_id":column_id})

    data_manager.execute_update(
        """
        UPDATE cards
        SET column_id = %(column_id)s, card_order = %(card_order)s
        WHERE id = %(card_id)s;
        """, {"card_id": card_id, "column_id": column_id, "card_order": card_order})


def get_status_id(column_name):
    status_id = data_manager.execute_select(
        """
        SELECT id
        FROM statuses
        WHERE status = %(column_name)s;
        """, {"column_name": column_name})
    return status_id[0]['id']


def add_new_status(column_name):
    data_manager.execute_update(
        """
        INSERT INTO statuses 
        (status)
        VALUES 
        (%(column_name)s); 
        """, {"column_name": column_name})


def get_last_column_number(board_id):
    max_order = data_manager.execute_select(
        """
        SELECT max(column_order)
        FROM columns
        WHERE board_id = %(board_id)s;
        """, {"board_id": board_id})[0]['max']
    return max_order


