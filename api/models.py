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

    def __init__(self):
        self.date_joined = None
        self.first_name = None
        self.email = None
        self.id = None
        self.pontuation = 0
        self.resource_uri = None
        self.username = None
