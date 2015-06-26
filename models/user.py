# Class user
from django.contrib.auth.models import User as DjangoUser
from django.db import models
import re


class User(DjangoUser):

    """User Model."""

    pontuation = models.IntegerField(default=0)

    def __unicode__(self):
        return str(self.username)

    @classmethod
    def all(cls):
        """Return all users."""
        return cls.objects.all()

    @classmethod
    def filter_by_username(cls, username):
        """Return all users containing specified username."""
        return cls.objects.filter(username=username)

    @classmethod
    def filter_by_email(cls, email):
        """Return all users containing specified email."""
        return cls.objects.filter(email=email)

    def validate_user_name(self):
        """Validate existing username"""
        if User.filter_by_username(self.username) is None:
            return True
        else:
            return False

    def validate_email(self):
        """Validate email regex."""
        if len(self.email) > 6:
            if re.match(r'\w[\w\.-]*@\w[\w\.-]+\.\w+', self.email) is not None:
                return True
        return False

    def validate_unique_email(self):
        """Validate unique email."""
        users = User.filter_by_email(self.email)
        if len(users) == 0:
            return True
        else:
            return False

    def validate_user_password(self, userpassword):
        """Validate password not blank."""
        if len(userpassword) == 0:
            return False
        else:
            return True
