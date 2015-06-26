# -*- coding utf-8 -*-
from django.db import models
from busline import Busline
from user import User


class Favorite (models.Model):

    """Favorite model"""

    user = models.ForeignKey(User)
    busline = models.ForeignKey(Busline)

    def __unicode__(self):
        """return comments of the favorite"""
        return 'User: %s, busline_id: %s' % (str(self.user_id),
                                             str(self.busline_id))

    @classmethod
    def all(cls):
        """return all objects of Favorite"""
        return cls.objects.all()

    @classmethod
    def favorites(cls, user_id):
        """return a list of favorites """
        return cls.objects.filter(user_id=user_id)

    @classmethod
    def is_favorite(cls, user_id, busline_id):
        """ Check if a busline is alredy favorited """
        count = cls.objects.filter(user_id=user_id, busline_id=busline_id)
        return count.count() != 0

    @classmethod
    def delete_favorite(cls, user_id, busline_id):
        """Delete a favorite busline """
        Favorite.objects.filter(
            user_id=user_id, busline_id=busline_id).delete()
