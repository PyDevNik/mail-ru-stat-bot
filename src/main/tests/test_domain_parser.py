import json
import unittest
import threading

from ..domain_parser import get_token, get_stats


class TestDomainParser(unittest.TestCase):
    def test_get_token(self):
        with open('main\\configuration.json') as config_file:
            config = json.load(config_file)
            refresh_token = config['refresh_token']

        for i in range(10):
            access_token = get_token(refresh_token)
            self.assertEqual(type(access_token), str)  # add assertion here

    def test_stress_get_token(self):
        def ask_token():
            with open('main\\configuration.json') as config_file:
                config = json.load(config_file)
                refresh_token = config['refresh_token']

            access_token = get_token(refresh_token)
            self.assertEqual(type(access_token), str)

        for i in range(1000):
            threading.Thread(target=ask_token).start()

    def test_get_stats(self):
        with open('main\\configuration.json') as config_file:
            config = json.load(config_file)
            refresh_token = config['refresh_token']
        DOMAIN = 'example.com'

        access_token = get_token(refresh_token)
        result = get_stats(DOMAIN, access_token)
        self.assertEqual(type(result), list)
        self.assertTrue(len(result) > 0)


if __name__ == '__main__':
    unittest.main()
