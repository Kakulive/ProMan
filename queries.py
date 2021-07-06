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
        """
        , {"status_id": status_id})

    return status


def get_boards():
    """
    Gather all boards
    :return:
    """
    return data_manager.execute_select(
        """
        SELECT * FROM boards
        ;
        """
    )


def get_cards_for_board(board_id):
    matching_cards = data_manager.execute_select(
        """
        SELECT * FROM cards
        WHERE cards.board_id = %(board_id)s
        ;
        """
        , {"board_id": board_id})

    return matching_cards


def save_user(username, email, hashed_password):
    registration_time = str(util.get_current_time())
    data_manager.execute_update(
        """
        INSERT INTO users
        (username, password, email, submission_time)
        VALUES 
        (%(username)s, %(password)s, %(email)s, %(submission_time)s)
        ;
        """
        , {"username": username, "password": hashed_password, "email": email, "submission_time": registration_time})
