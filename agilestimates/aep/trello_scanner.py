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
		log.append('Cards collected: ')
	except:
		log.append('Error connecting to trello')
	return (cards, log)
