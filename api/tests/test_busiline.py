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
        instance = Busline()
        self.assertIsNotNone(instance)
        instance = Terminal()
        self.assertIsNotNone(instance)
        instance = Company()
        self.assertIsNotNone(instance)

    def test_all(self):
        with self.assertRaises(BusinemeAPIConnectionError):
            self.busline.all()
        ret = json.loads(all())
        self.assertIsNotNone(self.busline._busline_list(ret))
