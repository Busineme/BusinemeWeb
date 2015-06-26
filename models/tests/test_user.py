# -*- coding: utf-8 -*-

from django.test import SimpleTestCase
from models.user import User


class TestUser(SimpleTestCase):

    def setUp(self):
        User.objects.all().delete()
        self.user = User()
        self.user.set_password('1234')
        self.user.username = 'test_name'
        self.user.email = "test@email.tes"
        self.user.save()

    def test_unicode(self):
        self.assertEquals(self.user.__unicode__(), "test_name")

    def test_all(self):
        db_before = User.all()
        User.objects.all().delete()
        db_after = User.all()
        self.assertTrue(db_after != db_before)

    def test_filter_by_username(self):
        users = User.filter_by_username("test_name")
        self.assertEquals(1, len(users))

    def test_filter_by_email(self):
        users = User.filter_by_email("test@email.tes")
        self.assertEquals(1, len(users))

    def set_email(self, email):
        self.user.email = email
        self.user.save()

    def set_nome(self, username):
        self.user.name = username
        self.user.username = username

    def test_validate_emaillessthansix(self):
        self.set_email("123")
        self.assertFalse(self.user.validate_email())

    def test_validate_emailinvalidregex(self):
        self.set_email("qwertyu")
        self.assertFalse(self.user.validate_email())

    def test_validate_email_valid_email(self):
        self.assertTrue(self.user.validate_email())

    def test_validate_user_name_invalid_name(self):
        self.set_nome(" ")
        self.assertFalse(self.user.validate_user_name())

    def test_validate_user_name_valid_name(self):
        self.assertFalse(self.user.validate_user_name())

    def test_validate_password_invalid_password(self):
        self.assertFalse(self.user.validate_user_password(""))

    def test_validate_password_valid_password(self):
        self.assertTrue(self.user.validate_user_password(" "))

    def test_not_unique_email(self):
        self.user.email = "test@email.tes"
        self.assertFalse(self.user.validate_unique_email())

    def test_unique_email_unique(self):
        self.user.email = "manusenac@hotmail.com"
        self.assertTrue(self.user.validate_unique_email())
