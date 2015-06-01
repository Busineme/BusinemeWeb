# -*- coding: utf-8 -*-
from api.models import User
from api.exception import BusinemeAPIConnectionError
from django.conf import settings
from requests.exceptions import ConnectionError
import requests
import json


class UserAPI(object):

    def all(self):
        url = settings.API_URL + 'user/'
        return self.__get_list(url)

    def create(self, user):
        assert type(user) == type(User())
        url = settings.API_URL + 'user/'
        user_data = json.dumps(user, default=lambda user: user.__dict__)
        headers = {'Content-type': 'application/json'}
        return requests.post(url, data=user_data, headers=headers)

    def __json_to_object(self, user_json):
        user = User()
        for attribute in user_json.keys():
            setattr(user, attribute, user_json[attribute])
        return user

    def __json_to_list(self, user_json):
        user_list = []
        for user in user_json['objects']:
            user_list.append(self.__json_to_object(user))
        return user_list

    def __get_list(self, url):
        try:
            user_json = requests.get(url).content
            user_json = json.loads(user_json)
            return self.__json_to_list(user_json)
        except ConnectionError, e:
            raise BusinemeAPIConnectionError(str(e))
