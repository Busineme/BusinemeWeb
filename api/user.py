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
        headers = {'Content-type': 'application/json'}
        return requests.post(url, data=self.__object_to_json(user),
                             headers=headers)

    def update(self, id, name=None, email=None, password=None):
        url = settings.API_URL + 'user/'
        user = User(id=id, first_name=name, email=email)
        user.set_password(password)
        headers = {'Content-type': 'application/json'}
        return requests.post(url, data=self.__object_to_json(user),
                             headers=headers)

    def __object_to_json(self, user):
        user_data = json.dumps(user, default=lambda user: user.__dict__)
        return user_data

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
