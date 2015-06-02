# -*- coding: utf-8 -*-


class Busline():

    """docstring for Busline"""
    def __init__(self):
        self.line_number = ""
        self.description = ""
        self.via = ""
        self.route_size = 0.0
        self.fee = 0.0
        self.company = None
        self.terminals = []


class Company():

    def __init__(self):
        self.name = ""


class Terminal():

    def __init__(self):
        self.description = ""
        self.address = ""


class User(object):

    def __init__(self, id=None, first_name=None, email=None, password=None):
        self.date_joined = None
        self.first_name = first_name
        self.email = email
        self.id = None
        self.pontuation = 0
        self.resource_uri = None
        self.username = None

    def set_password(self, password):
        self.password = password
