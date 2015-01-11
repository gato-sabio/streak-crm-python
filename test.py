# -*- coding: utf-8 -*-

from streak_crm_python import *
from keys import TEST_API_KEY
import unittest
import random
import string


class TestStreakConnection(unittest.TestCase):
    def setUp(self):
        self.alphanumeric_range = string.ascii_lowercase + '1234567890'
        self.supposed_endpoint = 'https://www.streak.com/api/v1/'
        self.my_email = 'robot@medperevod.com'

        self.normal_connection = StreakConnection()

        self.connections_with_wrong_api_key = StreakConnection(
            api_key=''.join([random.choice(self.alphanumeric_range) for character in self.alphanumeric_range])
        )

    def test_instance(self):
        self.assertIsInstance(self.normal_connection, object)

        self.assertIsInstance(self.connections_with_wrong_api_key, object)

    def test_settings(self):
        self.assertEqual(self.normal_connection.settings.api_key, TEST_API_KEY)
        self.assertEqual(self.normal_connection.settings.api_endpoint, self.supposed_endpoint)

        self.assertNotEqual(self.connections_with_wrong_api_key.settings.api_key, TEST_API_KEY)
        self.assertEqual(self.connections_with_wrong_api_key.settings.api_endpoint, self.supposed_endpoint)

    def test_normal_connection(self):
        self.assertEqual(self.normal_connection.user.me.email, self.my_email)

    def test_connections_with_wrong_api_key(self):
        self.assertEqual(self.connections_with_wrong_api_key.user.me.error, 'invalid api key')

    def test_user_get(self):
        test_user = self.normal_connection.user.get(
            'agxzfm1haWxmb29nYWVyMQsSDE9yZ2FuaXphdGlvbiIObWVkcGVyZXZvZC5jb20MCxIEVXNlchiAgIDQ98eFCgw')
        self.assertEqual(test_user.email , self.my_email)
        supposed_keys = ['tourId', 'creationTimestamp', 'lastUpdatedTimestamp', 'lastSavedTimestamp', 'lastSeenTimestamp',
                'installAppId', 'orgKey', 'contextIOStatus', 'userSettingsKey', 'email', 'isOauthComplete',
                'timezoneOffset', 'experiments']
        for key in supposed_keys:
            self.assertIn(key, test_user.__dict__)
        self.assertNotIn('foo', test_user.__dict__ )