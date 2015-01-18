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

    def pipeline_edit(self, pipeline_key: str, pipeline_params: dict):
        pipeline_update_result = self.post_api_data('pipelines/' + pipeline_key, json.dumps(pipeline_params))

        if 'success' in pipeline_update_result.keys():
            raise Exception(pipeline_update_result['error'])

        print('Pipeline updated')
        updated_pipeline = self.pipeline_get(pipeline_update_result['pipelineKey'])
        return updated_pipeline

    def box_get_all(self):
        boxes_list = []
        boxes_data = self.get_api_data('boxes/')
        for box_data in boxes_data:
            boxes_list.append(add_attributes(box_data, Box(self)))
        return boxes_list

    def box_get_all_in_pipeline(self, pipeline_key: str):
        boxes_list = []
        boxes_data = self.get_api_data('pipelines/%s/boxes' % pipeline_key)
        for box_data in boxes_data:
            boxes_list.append(add_attributes(box_data, Box(self)))
        return boxes_list

    def box_get(self, box_key: str):
        """
        Gets Box by key
        :param box_key:
        :return: Pipeline instance
        """
        if not box_key:
            raise Exception('[!] Empty box key, please supply one')

        box_data = self.get_api_data('boxes/' + box_key)

        if 'success' in box_data.keys():
            raise Exception(box_data['error'])

        box = add_attributes(box_data, Box(self))
        return box

    def box_create(self, pipeline_key: str, box_params: dict):
        """
        Creates and returns Box with given params
        :param box_params: dict of params
        :return: newly created Pipeline instance
        """
        box_data = self.put_api_data('pipelines/%s/boxes' % pipeline_key, box_params)

        if 'success' in box_data.keys():
            raise Exception(box_data['error'])

        new_box = self.box_get(box_data['boxKey'])

        print('New Box created')
        return new_box

    def box_delete(self, box_key: str):
        """
        Deletes Box by key
        :param box_key:
        :return:
        """
        response_on_delete = self.delete_api_data('boxes/' + box_key)

        if not response_on_delete['success']:
            raise Exception('Failed to delete Box')
        else:
            print('Box deleted')

    def box_edit(self, box_key: str, box_params: dict):
        box_update_result = self.post_api_data('boxes/' + box_key, json.dumps(box_params))

        if 'success' in box_update_result.keys():
            raise Exception(box_update_result['error'])

        print('Box updated')
        updated_box = self.box_get(box_update_result['boxKey'])
        return updated_box


class User:
    def __init__(self, streak_connection):
        self.streak_connection = streak_connection
        self.displayName = 'n/a'

    def __repr__(self):
        return '<User: %s>' % self.displayName

    # def reload(self):
    #     print('Updating User...'),
    #     self = self.streak_connection.user_get(self.userKey)
    #     print('...done.')
    #     return self


class Pipeline:
    def __init__(self, streak_connection):
        self.streak_connection = streak_connection
        self.name = ''
        self.pipelineKey = ''

    def __repr__(self):
        return '<Pipeline: %s>' % self.name

    # def reload(self):
    #     print('Updating Pipeline...'),
    #     self = self.streak_connection.pipeline_get(self.pipelineKey)
    #     print('...done.')
    #     return self


class Box:
    def __init__(self, streak_connection):
        self.streak_connection = streak_connection
        self.name = ''
        self.pipelineKey = ''

    def __repr__(self):
        return '<Box: %s>' % self.name



if __name__ == '__main__':
    pass