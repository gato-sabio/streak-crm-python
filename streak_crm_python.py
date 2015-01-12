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


def create_attrs(attr_dict, obj):
    """
    Makes dict items obj attributes
    :param attr_dict:
    :param obj:
    :return:
    """
    for key, value in attr_dict.items():
        setattr(obj, key, value)
    return obj


def api_get(self, request_path):
    return self.streak_connection.get_api_data(request_path)


class StreakConnection:
    def __init__(self, api_key=TEST_API_KEY):
        self.settings = self.Settings(api_key)
        self.user = self.User(self)
        self.pipeline = self.Pipeline(self)

    def __repr__(self):
        return '<Connection Obj %s>' % self.settings.api_key


    def get_api_data(self, api_path: str):
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

    class Settings:
        def __init__(self, api_key, api_endpoint='https://www.streak.com/api/v1/'):
            self.api_key = api_key
            self.api_endpoint = api_endpoint

    class User:
        def __init__(self, streak_connection):
            self.streak_connection = streak_connection
            self.displayName = 'not received yet'

        def __repr__(self):
            return '<User Obj: %s>' % self.displayName

        @property
        def me(self):
            request_path = 'users/me'
            attr_dict = api_get(self, request_path)
            new_user_instance = self.__class__(self.streak_connection)
            return create_attrs(attr_dict, new_user_instance)

        def get(self, user_key):
            """
            Gets User data by userKey
            :param user_key:
            :return:
            """
            request_path = 'users/' + user_key
            attr_dict = api_get(self, request_path)

            if 'success' in attr_dict.keys():
                raise Exception(attr_dict['error'])

            new_user_instance = self.__class__(self.streak_connection)
            return create_attrs(attr_dict, new_user_instance)

    class Pipeline:
        def __init__(self, streak_connection):
            self.streak_connection = streak_connection
            self.name = ''
            self.pipelineKey = ''

        def __repr__(self):
            # TODO return self via update?
            return '<Pipeline Obj: %s>' % self.name

        @property
        def all(self):
            pipelines_list = []
            pipeline_dicts = api_get(self, 'pipelines/')
            for pipeline_dict in pipeline_dicts:
                pipelines_list.append(create_attrs(pipeline_dict, self.__class__(self.streak_connection)))
            return pipelines_list

        def get(self, pipeline_key: str):
            if not pipeline_key:
                raise Exception('empty pipeline key')

            pipeline_dict = api_get(self, 'pipelines/' + pipeline_key)

            if 'success' in pipeline_dict.keys():
                raise Exception(pipeline_dict['error'])

            new_pipeline_instance = create_attrs(pipeline_dict, self.__class__(self.streak_connection))
            return new_pipeline_instance

        def create(self, settings: dict):
            api_path = 'pipelines/'
            new_pipeline = self.streak_connection.put_api_data(api_path, settings)

            if 'success' in new_pipeline.keys():
                raise Exception(new_pipeline['error'])

            print('[API PUT] New my_pipeline created with pipelineKey', new_pipeline['pipelineKey'])

            return self.get(new_pipeline['pipelineKey'])

        def delete(self, pipeline_key=''):
            if 'pipelineKey' in self.__dict__:
                api_path = 'pipelines/' + self.pipelineKey
            elif pipeline_key != '':
                api_path = 'pipelines/' + pipeline_key
            else:
                raise Exception("[!] Can't find my_pipeline key neither in instance nor in parameters")

            delete_result = self.streak_connection.delete_api_data(api_path)

            if not delete_result['success']:
                raise Exception('[HTTP DELETE] Failed to delete')
            else:
                print('[HTTP DELETE] Delete OK')

        def update(self, settings: str, pipeline_key=''):
            if 'pipelineKey' in self.__dict__:
                api_path = 'pipelines/' + self.pipelineKey
            elif pipeline_key != '':
                api_path = 'pipelines/' + pipeline_key
            else:
                raise Exception("[!] Can't find my_pipeline key neither in instance nor in parameters")

            pipeline_to_update = self.streak_connection.post_api_data(api_path, json.dumps(settings))

            if 'success' in pipeline_to_update.keys():
                raise Exception(pipeline_to_update['error'])

            print('[API POST] Pipeline updated')

            updated_pipeline = self.get(pipeline_to_update['pipelineKey'])
            self.name = updated_pipeline.name

            return updated_pipeline


if __name__ == '__main__':
    pass