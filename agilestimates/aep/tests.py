# -*- coding: utf-8 -*
from django.test import TestCase
from agilestimates.settings import trello_api_key, trello_auth_token
from mock import MagicMock, Mock
from trollop import TrelloConnection, Board, List, Card

import trello_scanner, encoding_utils, crypt_utils, trello_api

class TrelloApiTests(TestCase):
    def test_get_board(self):
        conn = TrelloConnection(trello_api_key, trello_auth_token)
        conn.get_board = MagicMock(return_value={'id': '12Hsd2', 'name': 'mocked board'})
        (status, board) = trello_api.get_board(conn, '12Hsd2')
        self.assertEqual(status, None)
        self.assertEqual(board['id'], '12Hsd2')
        self.assertEqual(board['name'], 'mocked board')

    def test_get_board_error(self):
        conn = TrelloConnection(trello_api_key, trello_auth_token)
        conn.get_board = Mock(side_effect=KeyError('error'))
        (status, board) = trello_api.get_board(conn, '12Hsd2')
        self.assertEqual(status, 'Could not get board')
        self.assertEqual(board, None)

    def test_get_done_list(self):
        conn = TrelloConnection(trello_api_key, trello_auth_token)
        l1 = List(conn, '1')
        l1.name = u'Backlog'
        l2 = List(conn, '2')
        l2.name = u'In progress'
        l3 = List(conn, '3')
        l3.name = u'Done'
        mocked_board = Board(conn, '1')
        mocked_board.lists = [l1, l2, l3]
        conn.get_board = MagicMock(return_value=mocked_board)
        (status, done_list) = trello_api.get_done_list(mocked_board)
        self.assertEqual(status, None)
        self.assertEqual(done_list.name, 'Done')

    def test_get_done_list_not_found(self):
        conn = TrelloConnection(trello_api_key, trello_auth_token)
        l1 = List(conn, '1')
        l1.name = u'Backlog'
        l2 = List(conn, '2')
        l2.name = u'In progress'
        l3 = List(conn, '3')
        l3.name = u'Fast Lane'
        mocked_board = Board(conn, '1')
        mocked_board.lists = [l1, l2, l3]
        conn.get_board = MagicMock(return_value=mocked_board)
        (status, done_list) = trello_api.get_done_list(mocked_board)
        self.assertEqual(status, 'Could not get done list')
        self.assertEqual(done_list, None)

    def test_get_list_cards(self):
        conn = TrelloConnection(trello_api_key, trello_auth_token)
        l1 = List(conn, '3')
        l1.name = u'Done'
        c1 = Card(conn, '1')
        c1.name = 'card1'
        c1.desc = 'desc for card1'
        c1.url = 'trello.com/c/19283ndks'
        c2 = Card(conn, '2')
        c2.name = 'card2'
        c2.desc = 'desc for card2'
        c2.url = 'trello.com/c/09sajkds'
        l1.cards = [c1, c2]
        mocked_board = Board(conn, '1')
        mocked_board.lists = [l1]
        conn.get_board = MagicMock(return_value=mocked_board)
        (status, done_list) = trello_api.get_done_list(mocked_board)
        (status, cards) = trello_api.get_list_cards(done_list)
        self.assertEqual(status, None)
        self.assertEqual(cards[0]['name'], 'card1')
        self.assertEqual(cards[0]['description'], 'desc for card1')
        self.assertEqual(cards[0]['url'], 'trello.com/c/19283ndks')
        self.assertEqual(cards[1]['name'], 'card2')
        self.assertEqual(cards[1]['description'], 'desc for card2')
        self.assertEqual(cards[1]['url'], 'trello.com/c/09sajkds')


class TrelloScannerTests(TestCase):
    def test_remove_label(self):
        result = trello_scanner.remove_label('Start Date: 2014-01-01')
        self.assertEqual(result, '2014-01-01')

    def test_remove_label_no_label_to_remove(self):
        result = trello_scanner.remove_label('2014-01-01')
        self.assertEqual(result, '2014-01-01')

    def test_get_field(self):
        splited_values = ['Start Date: 2014-01-01','Points: 3']
        result = trello_scanner.get_field(splited_values, 'Points')
        self.assertEqual(result, '3')

    def test_get_field_not_found(self):
        splited_values = ['Start Date: 2014-01-01','Points: 3']
        result = trello_scanner.get_field(splited_values, 'Unit Tests')
        self.assertIsNone(result)

    def test_count_points_delivered(self):
        cards_dict = [{'points': 2}, {'points': 9, 'start_date': '2014-01-01'}]
        total_points = trello_scanner.count_points_delivered(cards_dict)
        self.assertEqual(total_points, 11)

    def test_count_unit_tests(self):
        cards_dict = [{'unit_tests': 3}, {'unit_tests': 2, 'start_date': '2014-01-01'}]
        total_unit_tests = trello_scanner.count_unit_tests(cards_dict)
        self.assertEqual(total_unit_tests, 5)

    def test_summarize_metrics(self):
        cards_dict = [{'unit_tests': 3, 'points': 3}, {'unit_tests': 2, 'points': 9}]
        total_unit_tests, total_points_delivered = trello_scanner.summarize_metrics(cards_dict)
        self.assertEqual(total_unit_tests, 5)
        self.assertEqual(total_points_delivered, 12)

    def test_build_output_dict(self):
        card = {'description': 'Start Date: 2014-05-05\nEnd Date: 2014-05-08\nPoints: 2\nUnit Tests: 8\ntestestes\ntestestest\n', 'name': 'name1', 'url': 'http://www.mysite.com'}
        card_dict = trello_scanner.build_output_dict(card)
        self.assertEqual(card_dict['start_date'], '2014-05-05')
        self.assertEqual(card_dict['end_date'], '2014-05-08')
        self.assertEqual(card_dict['points'], '2')
        self.assertEqual(card_dict['unit_tests'], '8')

    def test_parse_cards(self):
        cards = []
        cards.append({'description': 'Start Date: 2014-05-05\nEnd Date: 2014-05-08\nPoints: 2\nUnit Tests: 8\ntestestes\ntestestest\n', 'name': 'name1', 'url': 'http://www.mysite.com'})
        cards.append({'description': 'Start Date: 2014-04-05\nEnd Date: 2014-04-08\nPoints: 4\nUnit Tests: 10\ntestestes\ntestestest\n', 'name': 'name1', 'url': 'http://www.mysite.com'})
        cards_dict = trello_scanner.parse_cards(cards)

        self.assertEqual(len(cards_dict), 2)
        self.assertEqual(cards_dict[0]['start_date'],'2014-05-05')
        self.assertEqual(cards_dict[1]['start_date'],'2014-04-05')

class TestEncodingUtils(TestCase):
    def test_normalize_value_unicode(self):
        result = encoding_utils.normalize_value(u'test')
        self.assertEqual(result, 'test')

    def test_normalize_value_string(self):
        result = encoding_utils.normalize_value('test')
        self.assertEqual(result, 'test')

    def test_remove_accents_with_accents(self):
        result = encoding_utils.remove_accents(u'tést')
        self.assertEqual(result, 'test')

    def test_remove_accents_without_accents(self):
        result = encoding_utils.remove_accents(u'test')
        self.assertEqual(result, 'test')


class TestCryptUtils(TestCase):
    def test_decrypt(self):
        decrypted_value = crypt_utils.decrypt('/2Ibeizz3eVDKw/bKpFiyjduhAD8hZyFEGo+DWyxwnWMw7Y6ZuWSzNz1x+x5HunC')
        self.assertEqual(decrypted_value, 't00thbrush')

    def test_encrypt(self):
        encrypted_value = crypt_utils.encrypt('t00thbrush')
        self.assertEqual(encrypted_value, 'MTIzNDU2Nzg5MDEyMzQ1NmWBGZkYjhye7jo8A+U4MHHu8QrIjC4HyuRlygvUiiP+')