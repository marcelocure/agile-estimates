#https://trello.com/docs/api/index.html
from agilestimates.settings import trello_api_key, trello_auth_token
from trollop import TrelloConnection
from encoding_utils import normalize_value


def get_connection():
	return TrelloConnection(trello_api_key, trello_auth_token)

def get_board(conn, board_id): 
	return conn.get_board(board_id)

def get_list(board, list_name): 
	result = filter(lambda l: str(l.name) == list_name, board.lists)
	return result[0]

def get_list_cards(t_list):
	return map(lambda card: {'name': normalize_value(card.name), 'description': normalize_value(card.desc), 'url': card.url}, t_list.cards)

def get_board_members(board):
	return map(lambda m: m.username, b.members)
