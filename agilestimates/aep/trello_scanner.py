from trello_api import get_connection, get_board, get_list, get_list_cards

def scan(trello_board_id):
    log = []
    cards = []
    log.append('Connecting to trello')
    try:
        conn = get_connection()
        log.append('Getting board')
        board = get_board(conn, trello_board_id)
        log.append('Getting Cards on list Done')
        t_list = get_list(board, 'Done')
        cards = get_list_cards(t_list)
        parse_cards(cards)
        log.append('Cards collected: ')
    except Exception as e:
        log.append('Error connecting to trello {0}'.format(e))
    return (cards, log)

def parse_cards(cards):
    try:
        for card in cards:
            description = card['description']
            splited_values = description.split('\n')
            print get_field(splited_values, 'Start Date:')
            print get_field(splited_values, 'End Date:')
            print get_field(splited_values, 'Points:')
            print get_field(splited_values, 'Unit Tests:')
    except Exception as e:
        print 'Error parsing cards {0}'.format(e)

def get_field(splited_values, field):
    result = filter(lambda row: field in row, splited_values)
    return result[0]