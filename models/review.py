# -*- coding: utf-8-*-
from django.db import models


class Review(models.Model):
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)
    review_type = models.IntegerField(default=0)

    def __unicode__(self):
        """Return comment of the review."""
        return self.comment

    @classmethod
    def filter_all(cls):
        """Return all reviews."""
        return cls.objects.all()
