# -*- coding: utf-8 -*-


class ApiException(Exception):

    """docstring for ExistingUser"""

    def __str__(self):
        return "API Connection Error"
