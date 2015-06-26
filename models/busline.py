# -*- coding: utf-8 -*-
""" docstring for package Busline """
from django.db import models as django_models
from api.busline import BuslineAPI
from exception.api import ApiException
import models


class Busline(django_models.Model):

    """Busline model."""

    def get_posts(self):
        return models.Post.objects.filter(
            busline=self).order_by("-date", "-time")

    line_number = django_models.CharField(max_length=5, unique=True)
    description = django_models.CharField(max_length=255)
    via = django_models.CharField(max_length=255)
    route_size = django_models.FloatField()  # unit: kilometers
    fee = django_models.DecimalField(
        decimal_places=2, max_digits=4)  # unit: BRL (R$)
    company = django_models.ForeignKey('Company', null=True)
    terminals = django_models.ManyToManyField('Terminal')
    posts = property(get_posts)

    def __unicode__(self):
        """Return line number and via."""
        return self.line_number + "-" + self.description

    @classmethod
    def all(cls):
        r"""
        If API is up, send requisition and returns all buslines. If API is \
        down, searches local database to return all buslines.
        """
        api = BuslineAPI()
        try:
            objects = api.all()
        except ApiException:
            objects = cls.objects.all()
        return objects

    @classmethod
    def filter_by_line_number(cls, line_number):
        r"""
        If API is up, send requisition and returns buslines with the \
        specified line number. If API is down, searches local database to\
        return buslines with the specified line number.
        """
        api = BuslineAPI()
        try:
            objects = api.filter_by_line(line_number)
        except ApiException:
            objects = cls.objects.filter(line_number__startswith=line_number)
        return objects

    @classmethod
    def filter_by_description(cls, description):
        r"""
        If API is up, send requisition and returns buslines with the \
        specified description. If API is down, searches local database to\
        return buslines with the specified description (via).
        """
        api = BuslineAPI()
        try:
            objects = api.filter_by_description(description)
        except ApiException:
            objects = cls.objects.filter(description__startswith=description)

        return objects

    @classmethod
    def filter_by_multiple(cls, line_number, description,
                           terminal__description):
        r"""
        Perform an advanced search filtering the results by the line number,\
        description and terminal description entered by the user then returns\
        the results list.
        """
        api = BuslineAPI()
        try:
            objects = api.filter(
                line_number=line_number,
                description=description,
                terminal__description=terminal__description
            )
        except ApiException:
            objects = cls.objects.filter(
                description__startswith=description,
                line_number__startswith=line_number,
                # terminals__startswith=terminals #FIXME forekey
            )

        return objects

    @classmethod
    def get_by_line_equals(cls, line_number):
        api = BuslineAPI()
        try:
            busline = api.get_by_line_equals(line_number)
        except:
            busline = cls.objects.get(line_number=line_number)
        return busline
