# -*- coding: utf-8 -*-

from streak_crm_python import *
from keys import TEST_API_KEY
import unittest
import random
import string
import datetime


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

        # def test_user_update(self):
        # me = self.streak.user_get_me()
        # me.reload()
        # # self.assNotIs


class TestCreateDeleteUpdatePipelines(unittest.TestCase):
    def setUp(self):
        """
        Creates, updates, deletes pipelines
        """
        self.streak = StreakConnection()

    def test_pipeline_create_and_update(self):
        self.settings = {
            'name': 'test name',
            'description': 'test description',
            'orgWide': True,
            'fieldNames': 'name, date, memo',
            'fieldTypes': 'PERSON, DATE, TEXT_INPUT',
            'stageNames': 'Cold Call, Meeting, Contract'
        }
        self.new_pipeline = self.streak.pipeline_create(self.settings)
        self.assertIsNotNone(self.new_pipeline.pipelineKey)

        self.assertEqual(self.new_pipeline.name, self.settings['name'])
        self.assertEqual(self.new_pipeline.description, self.settings['description'])
        self.assertEqual(self.new_pipeline.orgWide, self.settings['orgWide'])

        self.updated_settings = {
            'name': 'test name 2',
            'description': 'test description 2',
        }

        self.updated_pipeline = self.streak.pipeline_edit(self.new_pipeline.pipelineKey, self.updated_settings)
        # print(self.updated_pipeline.__dict__)

        self.assertEqual(self.updated_pipeline.name, self.updated_settings['name'])
        self.assertEqual(self.updated_pipeline.description, self.updated_settings['description'])


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
            self.new_pipeline = self.streak.pipeline_edit('12345', self.settings)


class TestCreateDeleteUpdateBoxes(unittest.TestCase):
    def setUp(self):
        """
        Creates, updates, deletes Boxes
        """
        self.streak = StreakConnection()


class TestCreateDeleteUpdateBoxes(unittest.TestCase):
    def setUp(self):
        """
        Creates, updates, deletes pipelines
        """
        self.streak = StreakConnection()
        self.pipeline = self.streak.pipeline_create(
            {
                'name': 'pipeline to test box',
                'description': 'test description',
                'orgWide': True,
                'fieldNames': 'name, date, memo',
                'fieldTypes': 'PERSON, DATE, TEXT_INPUT',
                'stageNames': 'Cold Call, Meeting, Contract'
            }
        )

    def test_box_create_and_update(self):
        box_settings = {
            'name': 'new_box',
            'notes': 'some notes',
        }

        # create box_1
        new_box_1 = self.streak.box_create(self.pipeline.pipelineKey, box_settings)

        # check if box params are updated on server
        self.assertEqual(new_box_1.name, box_settings['name'])
        self.assertEqual(new_box_1.notes, box_settings['notes'])

        updated_settings = {
            'name': 'new_box_1 changed',
            'notes': 'some notes 2'
        }

        # update params
        new_box_1 = self.streak.box_edit(new_box_1.boxKey, updated_settings)

        # check if box params are updated on server
        self.assertEqual(new_box_1.name, updated_settings['name'])
        self.assertEqual(new_box_1.notes, updated_settings['notes'])

        # create box_2
        new_box_2 = self.streak.box_create(self.pipeline.pipelineKey, {'name': 'another box', 'notes': 'somenotes'})

        self.boxes = self.streak.box_get_all()
        # print(self.boxes[0].__dict__)
        boxes_names = [box.name for box in self.boxes]
        boxes_notes = [box.notes for box in self.boxes]

        self.assertIn(new_box_1.name, boxes_names)
        self.assertIn(new_box_2.name, boxes_names)
        self.assertIn(new_box_1.notes, boxes_notes)
        self.assertIn(new_box_2.notes, boxes_notes)


    def tearDown(self):
        for box in self.boxes:
            box.delete_self()
        self.streak.pipeline_delete(self.pipeline.pipelineKey)