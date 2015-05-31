# -*- coding: utf-8 -*-
from api.models.busline import Busline
from api.models.company import Company
from api.models.terminal import Terminal
from api.exception import BusinemeAPIConnectionError
from django.conf import settings
import requests
import json


class BuslineAPI():

    def all(self):
        url = settings.API_URL + 'busline/'
        return self._get_filtered_list(url)

    def filter(self, **kwargs):
        url = settings.API_URL + 'busline/?'
        for name, value in kwargs.items():
            url += name + '__contains=' + value + '&'
        url += 'limit=0'
        return self._get_filtered_list(url)

    def filter_by_multiple(self, line_number, description):
        url = settings.API_URL + \
            'busline/?line_number__contains=' + line_number
        url += '&description__contains=' + description + '&limit=0'
        return self._get_filtered_list(url)

    def filter_by_line(self, line_number):
        url = settings.API_URL + 'busline/?line_number__contains=' + \
            line_number + '&limit=0'
        return self._get_filtered_list(url)

    def filter_by_description(self, description):
        url = settings.API_URL + 'busline/?description__contains=' + \
            description + '&limit=0'
        return self._get_filtered_list(url)

    def _get_filtered_list(self, url):
        try:
            busline_json = requests.get(url).content
            busline_json = json.loads(busline_json)
            return self._busline_list(busline_json)
        except Exception, e:
            raise BusinemeAPIConnectionError(str(e))

    def _company_json_to_object(self, company_json):
        company = Company()
        for attribute in company_json.keys():
            setattr(company, attribute, company_json[attribute])
        return company

    def _terminal_json_to_object(self, terminal_json):
        terminal = Terminal()
        for attribute in terminal_json.keys():
            setattr(terminal, attribute, terminal_json[attribute])
        return terminal

    def _terminals_list(self, terminals_json):
        terminals_list = []
        for terminal in terminals_json:
            terminals_list.append(self._terminal_json_to_object(terminal))
        return terminals_list

    def _json_to_object(self, busline_json):
        busline = Busline()
        for attribute in busline_json.keys():
            if attribute == 'company':
                setattr(busline, attribute,
                        self._company_json_to_object(busline_json[attribute]))
            elif attribute == 'terminals':
                setattr(busline, attribute,
                        self._terminals_list(busline_json[attribute]))
            else:
                setattr(busline, attribute, busline_json[attribute])

        return busline

    def _busline_list(self, busline_json):
        busline_list = []
        for busline in busline_json['objects']:
            busline_list.append(self._json_to_object(busline))

        return busline_list
