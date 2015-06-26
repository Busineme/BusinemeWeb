# -*- coding: utf-8 -*-

from django.test import SimpleTestCase
from models.terminal import Terminal


class TestTerminal(SimpleTestCase):

    def create_terminal(self):
        terminal = Terminal()
        terminal.description = "description"
        terminal.address = "address"
        terminal.save()
        return terminal

    def test_instance(self):
        terminal = Terminal()
        terminal = self.create_terminal()
        self.assertIsNotNone(terminal)

    def test_unicode(self):
        terminal = Terminal()
        terminal.description = "description"
        terminal.address = "address"
        terminal.save()
        self.assertEquals(terminal.__unicode__(), "description")

    def test_all(self):
        terminal = Terminal(description='description')
        self.assertIsNotNone(terminal.all())

    def test_filter_by_address(self):
        self.assertIsNotNone(
            Terminal.filter_by_address('Gama'))

    def test_saving_on_db(self):
        db_before = Terminal.objects.all()
        self.create_terminal()
        db_after = Terminal.objects.all()
        self.assertTrue(db_after != db_before)
