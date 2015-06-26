# -*- coding: utf-8 -*-
from django.db import models
from busline import Busline
from exception.line_without_post import LineWithoutPostError
from user import User
from terminal import Terminal


class Post(models.Model):

    """Busline model."""

    comment = models.CharField(max_length=255)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    traffic = models.IntegerField()
    capacity = models.IntegerField()
    busline = models.ForeignKey(Busline)
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)
    user = models.ForeignKey(User)
    terminal = models.ForeignKey(Terminal)

    def __unicode__(self):
        """Return comment of the post."""
        return 'id: %s date: %s %s busline: %s' % (self.id,
                                                   str(self.date),
                                                   str(self.time),
                                                   self.busline_id)

    @classmethod
    def all(cls):
        """Return all posts."""
        return cls.objects.all()

    @classmethod
    def last(cls, busline_id):
        """Return the last post from busline."""
        try:
            return cls.objects.filter(
                busline_id=busline_id).order_by("-date", "-time")[0]
        except:
            raise LineWithoutPostError()
