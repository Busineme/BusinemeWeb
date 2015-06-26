# -*- coding: utf-8 -*-
from api.models.busline import Busline
from api.models.company import Company
from api.models.terminal import Terminal
from django.conf import settings
from exception.api import ApiException
import requests
import json


class BuslineAPI(object):

    r"""
    BuslineAPI is a class that has methods to handle API requisitions for\
    the buslines.
    """

    def all(self):
        """Send requisition to get all buslines."""
        url = settings.API_URL + 'busline/'
        return self._get_filtered_list(url)

    def filter(self, **kwargs):
        r"""
        Send requisition to get buslines depending on the arguments. \
        This will be handled by the API, so only certain arguments names and \
        values can be handled.
        """
        url = settings.API_URL + 'busline/?'
        for name, value in kwargs.items():
            url += name + '__contains=' + value + '&'
        url += 'limit=0'
        return self._get_filtered_list(url)

    def filter_by_multiple(self, line_number, description):
        r"""
        Send requisition to get all buslines containing speficied line \
        number and description (via).
        """
        url = settings.API_URL + \
            'busline/?line_number__contains=' + line_number
        url += '&description__contains=' + description + '&limit=0'
        return self._get_filtered_list(url)

    def get_by_line_equals(self, line_number):
        url = settings.API_URL + 'busline/?line_number__exact=' + \
            line_number + '&limit=0'
        return self._get_filtered_list(url)[0]

    def filter_by_line(self, line_number):
        r"""
        Send requisition to get all buslines containing speficied \
        line number.
        """
        url = settings.API_URL + 'busline/?line_number__contains=' + \
            line_number + '&limit=0'
        return self._get_filtered_list(url)

    def filter_by_description(self, description):
        r"""
        Send requisition to get all buslines containing speficied \
        description (via).
        """
        url = settings.API_URL + 'busline/?description__contains=' + \
            description + '&limit=0'
        return self._get_filtered_list(url)

    def _get_filtered_list(self, url):
        r"""
        Load the json returned by the requisition and then ruturns the objects.
        """
        try:
            buslines = requests.get(url)
            return self._busline_list(buslines.json())
        except Exception, e:
            raise ApiException(str(e))

    def _company_json_to_object(self, company_json):
        """Parse the company, inside the json, to object"""

        company = Company()
        for attribute in company_json.keys():
            setattr(company, attribute, company_json[attribute])
        return company

    def _terminal_json_to_object(self, terminal_json):
        """Parse the terminal, inside the json, to object."""

        terminal = Terminal()
        for attribute in terminal_json.keys():
            setattr(terminal, attribute, terminal_json[attribute])
        return terminal

    def _terminals_list(self, terminals_json):
        r"""
        Parse the terminals, inside the json, to objects (plural), since\
        its a list.
        """
        terminals_list = []
        for terminal in terminals_json:
            terminals_list.append(self._terminal_json_to_object(terminal))
        return terminals_list

    def _json_to_object(self, busline_json):
        r"""
        Parse the busline, inside the json, to object, with proper terminals\
        and companies.
        """
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
        r"""
        Parse the buslines, inside the json, to objects (plural), since\
        its a list.
        """
        busline_list = []
        for busline in busline_json["objects"]:
            busline_list.append(self._json_to_object(busline))

        return busline_list
