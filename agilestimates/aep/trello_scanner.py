from trello_api import get_connection, get_board, get_done_list, get_list_cards
from models import Card, Sprint
import traceback

def scan(trello_board_id):
    try:
        log = []
        status, conn = get_connection()
        if conn is None:
            log.append(status)
            return (True, None, log, None, None, None)
        log.append('Reading board')

        status, board = get_board(conn, trello_board_id)
        if board is None:
            log.append(status)
            return (True, None, log, None, None, None)

        status, t_list = get_done_list(board)
        if t_list is None:
            log.append(status)
            return (True, None, log, None, None, None)

        status, cards = get_list_cards(t_list)
        if cards is None:
            log.append(status)
            return (True, None, log, None, None, None)

        cards_dict = parse_cards(cards)
        #for c in cards_dict:
        #    print c
        card_list = create_card_list(cards_dict)
        total_unit_tests, total_points_delivered = summarize_metrics(cards_dict)
        log.append('Cards collected: ')
        return (False, cards, log, total_unit_tests, total_points_delivered, card_list)
    except Exception as e:
        log.append('Error connecting to trello {0}'.format(e))
        print traceback.format_exc()

def summarize_metrics(cards_dict):
    total_unit_tests = count_unit_tests(cards_dict)
    total_points_delivered = count_points_delivered(cards_dict)
    return (total_unit_tests, total_points_delivered)

def count_unit_tests(cards_dict):
    total_unit_tests = 0
    for card_dict in cards_dict:
        total_unit_tests = total_unit_tests + int(card_dict['unit_tests'])
    return total_unit_tests

def count_points_delivered(cards_dict):
    total_points_delivered = 0
    for card_dict in cards_dict:
        total_points_delivered = total_points_delivered + float(card_dict['points'])
    return total_points_delivered

def parse_cards(cards):
    return map(build_output_dict, cards)

def create_card_list(cards_dict):
    return map(bind_card, cards_dict)

def bind_card(card_dict):
    card = None
    try:
        card = Card(sprint=Sprint(),
                    name=card_dict['name'],
                    url=card_dict['url'],
                    description=card_dict['description'],
                    start_date=card_dict['start_date'],
                    end_date=card_dict['end_date'],
                    points_created=card_dict['points'],
                    tests_created=card_dict['unit_tests'])
    except Exception as e:
        print e
    return card

def build_output_dict(card):
    name = card['name']
    description = card['description']
    url = card['url']
    splited_values = description.split('\n')
    start_date = get_field(splited_values, 'Start Date:')
    end_date = get_field(splited_values, 'End Date:')
    points = get_field(splited_values, 'Points:')
    unit_tests = get_field(splited_values, 'Unit Tests:')
    return {'url': url, 'name':name, 'description':description, 'start_date':start_date, 'end_date':end_date, 'points':points, 'unit_tests':unit_tests}

def get_field(splited_values, field):
    result = filter(lambda row: field in row, splited_values)
    if len(result) == 0:
        return None
    return remove_label(result[0])

def remove_label(result):
    position = result.find(':')
    if position < 0:
        return result
    return result[position+2:]
