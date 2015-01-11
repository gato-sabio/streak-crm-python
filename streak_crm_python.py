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


def write_attributes(attr_dict, obj):
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
    return self.streak_connection.read_api_data(request_path)


class StreakConnection:
    def __init__(self, api_key=TEST_API_KEY):
        self.settings = self.Settings(api_key)
        self.user = self.User(self)
        self.pipeline = self.Pipeline(self)

    def read_api_data(self, api_path: str):
        api_full_path = self.settings.api_endpoint + api_path
        print(api_full_path)
        try:
            result = requests.get(api_full_path, auth=HTTPBasicAuth(self.settings.api_key, ''))
        except requests.HTTPError:
            print('[HTTP] Error')
            result = None
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

        @property
        def me(self):
            flush_attributes(self)
            request_path = 'users/me'
            attr_dict = api_get(self, request_path)
            # if 'attr_dict'
            return write_attributes(attr_dict, self)

        def get(self, user_key):
            """
            Gets User data by userKey
            :param user_key:
            :return:
            """
            flush_attributes(self)
            request_path = 'users/' + user_key
            attr_dict = api_get(self, request_path)
            return write_attributes(attr_dict, self)

    class Pipeline:
        def __init__(self, streak_connection):
            self.streak_connection = streak_connection

        @property
        def all(self):
            return api_get(self, 'pipelines/')

        def get(self, pipeline_key):
            return api_get(self, 'pipelines/' + pipeline_key)

if __name__ == '__main__':
    pass