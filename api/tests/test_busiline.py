# -*- coding: utf-8 -*-
from api.busline import BuslineAPI
from api.models import *
from api.exception import BusinemeAPIConnectionError
from django.test import SimpleTestCase
import json


def all():
    f = open('api/tests/out.json', 'r')
    data = f.read()
    f.close()
    return data


class testBusilineAPI(SimpleTestCase):

    """docstring for testBusilineAPI"""

    def setUp(self):
        self.busline = BuslineAPI()

    def test_models(self):
        instance = busline.Busline()
        self.assertIsNotNone(instance)
        instance = terminal.Terminal()
        self.assertIsNotNone(instance)
        instance = company.Company()
        self.assertIsNotNone(instance)

    def test_all(self):
        from requests import *
        from requests.sessions import *
        with self.assertRaises(BusinemeAPIConnectionError):
            self.busline.all()
        ret = json.loads(all())
        self.assertIsNotNone(self.busline._busline_list(ret))
