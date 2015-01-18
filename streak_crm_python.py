# -*- coding: utf-8 -*-

import json
import requests
from requests.auth import HTTPBasicAuth

from keys import TEST_API_KEY


def flush_attributes(obj):
    tmp = obj.__dict__['streak_connection']
    obj.__dict__ = {}
    setattr(obj, 'streak_connection', tmp)
    return obj


def add_attributes(attr_dict, obj):
    """
    Takes obj and dict, creates obj properties as dict keys:values , returns obj updated
    # >>> add_attributes({'fox_count': 15}, animal_counter)
    # >>> animal_counter.fox_count == 15
    # True
    :param attr_dict: dict with attrs
    :param obj: object
    :return: obj updated
    """
    for key, value in attr_dict.items():
        setattr(obj, key, value)
    return obj


# def api_get(self, request_path):
# return self.streak_connection.get_api_data(request_path)


class StreakConnection:
    def __init__(self, api_key=TEST_API_KEY):
        self.settings = self.Settings(api_key)

    def __repr__(self):
        return '<StreakConnection Object: %>'

    class Settings:
        def __init__(self, api_key, api_endpoint='https://www.streak.com/api/v1/'):
            self.api_key = api_key
            self.api_endpoint = api_endpoint

    def get_api_data(self, api_path: str):
        """
        Merges api_endpoint with api_path and sends GET request
        :param api_path: string
        :return: object
        """
        result = None
        api_full_path = self.settings.api_endpoint + api_path
        print('[API GET]', api_full_path)
        try:
            result = requests.get(api_full_path, auth=HTTPBasicAuth(self.settings.api_key, ''))
        except requests.HTTPError:
            print('[HTTP GET] Error')
            exit()
        else:
            result = json.loads(result.text)
        return result

    def put_api_data(self, api_path: str, settings: dict):
        """
        Merges api_endpoint with api_path and sends PUT request
        :param api_path: string
        :return: object
        """
        result = None
        api_full_path = self.settings.api_endpoint + api_path
        print('[API PUT]', api_full_path)
        try:
            result = requests.put(api_full_path, data=settings, auth=HTTPBasicAuth(self.settings.api_key, ''))
        except requests.HTTPError:
            print('[HTTP PUT] Error')
            exit()
        else:
            result = json.loads(result.text)
        return result

    def delete_api_data(self, api_path: str):
        """
        Merges api_endpoint with api_path and sends DELETE request
        :param api_path: string
        :return: object
        """
        result = None
        api_full_path = self.settings.api_endpoint + api_path
        print('[API DELETE]', api_full_path)
        try:
            result = requests.delete(api_full_path, auth=HTTPBasicAuth(self.settings.api_key, ''))
        except requests.HTTPError:
            print('[HTTP DELETE] Error')
            exit()
        else:
            result = json.loads(result.text)
        return result

    def post_api_data(self, api_path: str, settings: json):
        """
        Merges api_endpoint with api_path and sends POST request
        :param api_path: string
        :return: object
        """
        result = None
        api_full_path = self.settings.api_endpoint + api_path
        print('[API POST]', api_full_path)
        try:
            result = requests.post(api_full_path, data=settings, auth=HTTPBasicAuth(self.settings.api_key, ''),
                                   headers={'Content-Type': 'application/json'})
        except requests.HTTPError:
            print('[HTTP POST] Error')
            exit()
        else:
            result = json.loads(result.text)
        return result

    def user_get_me(self):
        """
        Returns current authorized User (myself)
        :return: User
        """
        request_path = 'users/me'
        user_me_data = self.get_api_data(request_path)
        # creates new User instance as assigns keys:values from server response as it's properties
        user = add_attributes(user_me_data, User(self))
        return user

    def user_get(self, user_key):
        """
        Gets User data by userKey
        :param user_key: string
        :return: User
        """
        request_path = 'users/' + user_key
        user_data = self.get_api_data(request_path)

        # if server response has error code
        if 'success' in user_data.keys():
            raise Exception(user_data['error'])

        user = add_attributes(user_data, User(self))
        return user

    def pipeline_get_all(self):
        """
        Gets all pipelines
        :return: list of Pipelines objects
        """
        pipelines_list = []
        request_path = 'pipelines/'
        pipelines_data = self.get_api_data('pipelines/')
        for pipeline_dict in pipelines_data:
            pipelines_list.append(add_attributes(pipeline_dict, Pipeline(self)))
        return pipelines_list

    def pipeline_get(self, pipeline_key: str):
        """
        Gets Pipeline by key
        :param pipeline_key:
        :return: Pipeline instance
        """
        if not pipeline_key:
            raise Exception('[!] Empty pipeline key, please supply one')

        pipeline_data = self.get_api_data('pipelines/' + pipeline_key)

        if 'success' in pipeline_data.keys():
            raise Exception(pipeline_data['error'])

        pipeline = add_attributes(pipeline_data, Pipeline(self))
        return pipeline

    def pipeline_create(self, pipeline_params: dict):
        """
        Creates and returns Pipeline with given params
        :param pipeline_params: dict of params
        :return: newly created Pipeline instance
        """
        pipeline_data = self.put_api_data('pipelines/', pipeline_params)

        if 'success' in pipeline_data.keys():
            raise Exception(pipeline_data['error'])

        new_pipeline = self.pipeline_get(pipeline_data['pipelineKey'])

        print('New Pipeline created')

        return new_pipeline

    def pipeline_delete(self, pipeline_key: str):
        """
        Deletes pipeline by key
        :param pipeline_key:
        :return:
        """
        response_on_delete = self.delete_api_data('pipelines/' + pipeline_key)

        if not response_on_delete['success']:
            raise Exception('Failed to delete Pipeline')
        else:
            print('Pipeline deleted')

    def pipeline_update(self, pipeline_key: str, pipeline_params: dict):
            pipeline_update_result = self.post_api_data('pipelines/' + pipeline_key, json.dumps(pipeline_params))

            if 'success' in pipeline_update_result.keys():
                raise Exception(pipeline_update_result['error'])

            print('Pipeline updated')
            updated_pipeline = self.pipeline_get(pipeline_update_result['pipelineKey'])
            return updated_pipeline


class User:
    def __init__(self, streak_connection):
        self.streak_connection = streak_connection
        self.displayName = 'n/a'

    def __repr__(self):
        return '<User: %s>' % self.displayName


class Pipeline:
    def __init__(self, streak_connection):
        self.streak_connection = streak_connection
        self.name = ''
        self.pipelineKey = ''

    def __repr__(self):
        return '<Pipeline: %s>' % self.name


# class Box:
# def __init__(self, streak_connection):
# self.streak_connection = streak_connection
#         self.name = ''
#         self.pipelineKey = ''
#
#     def __repr__(self):
#         return '<Box Obj: %s>' % self.name
#
#     @property
#     def all(self):
#         boxes_list = []
#         boxes_dicts = self.streak_connection.get_api_data('boxes/')
#         for box_dict in boxes_dicts:
#             boxes_list.append(add_attributes(box_dict, self.__class__(self.streak_connection)))
#         return boxes_list
#
#     @property
#     def all_in_pipeline(self, pipeline_key=''):
#         if 'pipelineKey' in self.__dict__:
#             api_path = 'pipelines/%s/boxes' % self.pipelineKey
#         elif pipeline_key != '':
#             api_path = 'pipelines/%s/boxes' % pipeline_key
#         else:
#             raise Exception("[!] Can't find new_pipeline key neither in instance nor in parameters")
#
#         boxes_list = []
#         boxes_dicts = self.streak_connection.get_api_data(api_path)
#         for box_dict in boxes_dicts:
#             boxes_list.append(add_attributes(box_dict, self.__class__(self.streak_connection)))
#         return boxes_list
#

if __name__ == '__main__':
    pass