# -*- coding: utf-8 -*-


class BusinemeAPIConnectionError(Exception):

    def __str__(self):
        return 'Could not connect to the BusinemeAPI'
