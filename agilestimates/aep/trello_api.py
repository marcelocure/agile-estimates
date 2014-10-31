#https://trello.com/docs/api/index.html
from agilestimates.settings import trello_api_key, trello_auth_token
from trollop import TrelloConnection
from encoding_utils import normalize_value
import traceback
import unicodedata


def get_connection():
    try:
        return (None, TrelloConnection(trello_api_key, trello_auth_token))
    except:
        print traceback.format_exc()
        return ('could not get conection', None)

def get_board(conn, board_id): 
    try:
        return (None, conn.get_board(board_id))
    except:
        print traceback.format_exc()
        return ('could not get board', None)

def get_done_list(board):
    try:
        result = filter(lambda l: remove_accents(l.name) in ['Done', 'Aceite'], board.lists)
        return (None, result[0])
    except Exception as e:
        print traceback.format_exc()
        return ('Done List not found', None)

def get_list_cards(t_list):
    try:
        return (None, map(lambda card: {'name': normalize_value(card.name), 'description': normalize_value(card.desc), 'url': card.url}, t_list.cards))
    except:
        print traceback.format_exc()
        return ('could not get list cards', None)

def remove_accents(input_str):
    nkfd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nkfd_form.encode('ASCII', 'replace')
    return only_ascii
