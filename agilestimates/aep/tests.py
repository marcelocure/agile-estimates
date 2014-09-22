from django.test import TestCase
import trello_scanner, encoding_utils, crypt_utils

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

class TestCryptUtils(TestCase):
    def test_decrypt(self):
        decrypted_value = crypt_utils.decrypt('/2Ibeizz3eVDKw/bKpFiyjduhAD8hZyFEGo+DWyxwnWMw7Y6ZuWSzNz1x+x5HunC')
        self.assertEqual(decrypted_value, 't00thbrush')

    def test_encrypt(self):
        encrypted_value = crypt_utils.encrypt('t00thbrush')
        self.assertEqual(encrypted_value, 'MTIzNDU2Nzg5MDEyMzQ1NmWBGZkYjhye7jo8A+U4MHHu8QrIjC4HyuRlygvUiiP+')