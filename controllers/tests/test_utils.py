# -*- coding: utf-8 -*-

from django.test import SimpleTestCase, RequestFactory
from django.http import HttpRequest
from controllers.utils import modal_message


class TestUtils(SimpleTestCase):

    def setUp(self):
        self.request = HttpRequest()
        self.data = {"name": "user_test", "email": "email@test.com",
                     "username": "usermane_test", "password": "1234"}
        self.STATUS_OK = 200
        self.STATUS_REDIRECT = 302
        self.factory = RequestFactory()

    def test_error_message_status_code(self):
        error = "errortest"
        response = modal_message(
            error, error, error, "register_user_page.html", self.request)
        self.assertEquals(response.status_code, self.STATUS_OK)
