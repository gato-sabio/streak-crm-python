# -*- coding: utf-8 -*-

from streak_crm_python import *
from keys import TEST_API_KEY
import unittest
import random
import string


alphanumeric_range = string.ascii_lowercase + '1234567890'
supposed_endpoint = 'https://www.streak.com/api/v1/'
my_email = 'robot@medperevod.com'


class TestStreakConnection(unittest.TestCase):
    def setUp(self):
        self.normal_connection = StreakConnection()

        self.connections_with_wrong_api_key = StreakConnection(
            api_key=''.join([random.choice(alphanumeric_range) for character in alphanumeric_range])
        )

    def test_instance(self):
        self.assertIsInstance(self.normal_connection, object)

        self.assertIsInstance(self.connections_with_wrong_api_key, object)

    def test_settings(self):
        self.assertEqual(self.normal_connection.settings.api_key, TEST_API_KEY)
        self.assertEqual(self.normal_connection.settings.api_endpoint, supposed_endpoint)

        self.assertNotEqual(self.connections_with_wrong_api_key.settings.api_key, TEST_API_KEY)
        self.assertEqual(self.connections_with_wrong_api_key.settings.api_endpoint, supposed_endpoint)

    def test_normal_connection(self):
        self.assertEqual(self.normal_connection.user.me.email, my_email)

    def test_connections_with_wrong_api_key(self):
        self.assertEqual(self.connections_with_wrong_api_key.user.me.error, 'invalid api key')


class TestUsers(unittest.TestCase):
    def setUp(self):
        self.streak = StreakConnection()

    def test_user_me(self):
        self.me = self.streak.user.me
        self.assertEqual(self.me.email, my_email)

    def test_user_get(self):
        test_user = self.streak.user.get(
            'agxzfm1haWxmb29nYWVyMQsSDE9yZ2FuaXphdGlvbiIObWVkcGVyZXZvZC5jb20MCxIEVXNlchiAgIDQ98eFCgw')
        self.assertEqual(test_user.email, my_email)
        supposed_keys = ['tourId', 'creationTimestamp', 'lastUpdatedTimestamp', 'lastSavedTimestamp',
                         'lastSeenTimestamp',
                         'installAppId', 'orgKey', 'contextIOStatus', 'userSettingsKey', 'email', 'isOauthComplete',
                         'timezoneOffset', 'experiments']
        for key in supposed_keys:
            self.assertIn(key, test_user.__dict__)
        self.assertNotIn('foo', test_user.__dict__)


class TestCreateDeleteUpdatePipelines(unittest.TestCase):
    def setUp(self):
        self.streak = StreakConnection()

    def test_create(self):
        self.settings = {
            'name': 'test name',
            'description': 'test description',
            'orgWide': True,
            'fieldNames': 'name, date, memo',
            'fieldTypes': 'PERSON, DATE, TEXT_INPUT',
            'stageNames': 'Cold Call, Meeting, Contract'
        }
        self.my_pipeline = self.streak.pipeline.create(settings=self.settings)
        self.assertIsNotNone(self.my_pipeline.pipelineKey)

        self.assertEqual(self.my_pipeline.name, self.settings['name'])
        self.assertEqual(self.my_pipeline.description, self.settings['description'])
        self.assertEqual(self.my_pipeline.orgWide, self.settings['orgWide'])

        self.updated_settings = {
            'name': 'test name 2',
            'description': 'test description 2',
            'orgWide': False,
            'fieldNames': 'name 2, date 2, memo',
            'fieldTypes': 'PERSON, DATE, TEXT_INPUT',
            'stageNames': 'Cold Call 2, Meeting 2, Contract 2'
        }

        self.my_pipeline.update(settings=self.updated_settings)

        self.assertEqual(self.my_pipeline.name, self.settings['name'])
        self.assertEqual(self.my_pipeline.description, self.settings['description'])
        self.assertEqual(self.my_pipeline.orgWide, self.settings['orgWide'])


    def tearDown(self):
        self.my_pipeline.delete()


class TestCreateDeleteUpdatePipelinesWithInvalidParams(unittest.TestCase):
    def setUp(self):
        self.streak = StreakConnection()

    def test_get_invalid_params(self):
        with self.assertRaisesRegex(Exception, 'Illegal Argument Exception in GetEntities, usually a key issue'):
            self.my_pipeline = self.streak.pipeline.get('12345')
        with self.assertRaisesRegex(Exception, 'empty pipeline key'):
            self.my_pipeline = self.streak.pipeline.get('')

    def test_create_invalid_params(self):
        self.settings = {
            'foo name': 'test name',
            'description': 'test description',
        }

        with self.assertRaisesRegex(Exception, 'Insufficient params for Pipeline'):
            self.my_pipeline = self.streak.pipeline.create(settings=self.settings)

        with self.assertRaisesRegex(Exception, 'Failed to delete'):
            self.my_pipeline = self.streak.pipeline.delete('12345')

        with self.assertRaisesRegex(Exception, 'existing entity does not exist'):
            self.my_pipeline = self.streak.pipeline.update(settings=self.settings, pipeline_key='12345')
