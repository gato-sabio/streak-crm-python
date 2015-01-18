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
        """
        Create normal and abnormal connections
        :return:
        """
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
        self.assertEqual(self.normal_connection.user_get_me().email, my_email)

    def test_connections_with_wrong_api_key(self):
        self.assertEqual(self.connections_with_wrong_api_key.user_get_me().error, 'invalid api key')


class TestUsers(unittest.TestCase):
    def setUp(self):
        self.streak = StreakConnection()

    def test_user_me(self):
        me = self.streak.user_get_me()
        print('Me:', me)
        self.assertEqual(me.email, my_email)
        # print('me._dict__:', me.__dict__)

    def test_user_get(self):
        user = self.streak.user_get(
            'agxzfm1haWxmb29nYWVyMQsSDE9yZ2FuaXphdGlvbiIObWVkcGVyZXZvZC5jb20MCxIEVXNlchiAgIDQ98eFCgw')
        self.assertEqual(user.email, my_email)
        supposed_keys = ['tourId', 'creationTimestamp', 'lastUpdatedTimestamp', 'lastSavedTimestamp',
                         'lastSeenTimestamp',
                         'installAppId', 'orgKey', 'contextIOStatus', 'userSettingsKey', 'email', 'isOauthComplete',
                         'timezoneOffset', 'experiments']
        for key in supposed_keys:
            self.assertIn(key, user.__dict__)
        self.assertNotIn('foo', user.__dict__)


class TestCreateDeleteUpdatePipelines(unittest.TestCase):
    def setUp(self):
        """
        Creates, updates, deletes pipelines
        """
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
        self.new_pipeline = self.streak.pipeline_create(pipeline_params=self.settings)
        # print(self.new_pipeline.__dict__)
        self.assertIsNotNone(self.new_pipeline.pipelineKey)

        self.assertEqual(self.new_pipeline.name, self.settings['name'])
        self.assertEqual(self.new_pipeline.description, self.settings['description'])
        self.assertEqual(self.new_pipeline.orgWide, self.settings['orgWide'])

        self.updated_settings = {
            'name': 'test name 2',
            'description': 'test description 2',
            'orgWide': False,
            'fieldNames': 'name 2, date 2, memo',
            'fieldTypes': 'PERSON, DATE, TEXT_INPUT',
            'stageNames': 'Cold Call 2, Meeting 2, Contract 2'
        }

        self.streak.pipeline_update(self.new_pipeline.pipelineKey, self.updated_settings)

        self.assertEqual(self.new_pipeline.name, self.settings['name'])
        self.assertEqual(self.new_pipeline.description, self.settings['description'])
        self.assertEqual(self.new_pipeline.orgWide, self.settings['orgWide'])


    def tearDown(self):
        self.streak.pipeline_delete(self.new_pipeline.pipelineKey)


class TestCreateDeleteUpdatePipelinesWithInvalidParams(unittest.TestCase):
    def setUp(self):
        """
        Creates, updates, deletes pipelines with invalid parameters
        """
        self.streak = StreakConnection()

    def test_get_invalid_params(self):
        with self.assertRaisesRegex(Exception, 'Illegal Argument Exception in GetEntities, usually a key issue'):
            self.new_pipeline = self.streak.pipeline_get('12345')
        with self.assertRaisesRegex(Exception, 'Empty pipeline key, please supply one'):
            self.new_pipeline = self.streak.pipeline_get('')

    def test_create_invalid_params(self):
        self.settings = {
            'foo name': 'test name',
            'description': 'test description',
        }

        with self.assertRaisesRegex(Exception, 'Insufficient params for Pipeline'):
            self.new_pipeline = self.streak.pipeline_create(self.settings)

        with self.assertRaisesRegex(Exception, 'Failed to delete'):
            self.new_pipeline = self.streak.pipeline_delete('12345')

        with self.assertRaisesRegex(Exception, 'existing entity does not exist'):
            self.new_pipeline = self.streak.pipeline_update('12345', self.settings)
