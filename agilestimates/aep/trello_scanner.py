from trello_api import get_connection, get_board, get_list, get_list_cards

def scan(trello_board_id):
    log = []
    cards = []
    total_unit_tests = 0
    total_points_delivered = 0
    log.append('Connecting to trello')
    try:
        conn = get_connection()
        log.append('Getting board')
        board = get_board(conn, trello_board_id)
        log.append('Getting Cards on list Done')
        t_list = get_list(board, 'Done')
        cards = get_list_cards(t_list)
        cards_dict = parse_cards(cards)
        total_unit_tests, total_points_delivered = summarize_metrics(cards_dict)
        print (total_unit_tests, total_points_delivered)
        log.append('Cards collected: ')
    except Exception as e:
        log.append('Error connecting to trello {0}'.format(e))
    return (cards, log, total_unit_tests, total_points_delivered)

def summarize_metrics(cards_dict):
    total_unit_tests = count_unit_tests(cards_dict)
    total_points_delivered = count_unit_tests(cards_dict)
    return (total_unit_tests, total_points_delivered)

def count_unit_tests(cards_dict):
    total_unit_tests = 0
    for card_dict in cards_dict:
        total_unit_tests = total_unit_tests + int(card_dict['unit_tests'])
    return total_unit_tests

def count_points_delivered(cards_dict):
    total_points_delivered = 0
    for card_dict in cards_dict:
        total_points_delivered = total_points_delivered + int(card_dict['unit_tests'])
    return total_points_delivered

def parse_cards(cards):
    return map(build_output_dict, cards)

def build_output_dict(card):
    description = card['description']
    splited_values = description.split('\n')
    start_date = get_field(splited_values, 'Start Date:')
    end_date = get_field(splited_values, 'End Date:')
    points = get_field(splited_values, 'Points:')
    unit_tests = get_field(splited_values, 'Unit Tests:')
    return {'start_date':start_date, 'end_date':end_date, 'points':points, 'unit_tests':unit_tests}

def get_field(splited_values, field):
    result = filter(lambda row: field in row, splited_values)
    return remove_label(result[0])

def remove_label(result):
    position = result.find(':')+2
    return result[position:]