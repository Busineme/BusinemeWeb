# -*- coding: utf-8 -*-

from django.test import SimpleTestCase
from models.review import Review


class TestReview(SimpleTestCase):

    """docstring for TestReview"""

    def test_unicode(self):
        review = Review()
        review.comment = "comment"
        review.save()
        self.assertEquals(review.__unicode__(), "comment")

    def test_filter_all(self):
        review = Review()
        self.assertIsNotNone(review.filter_all())

    def test_atributes(self):
        review = Review()
        review.save()
        self.assertIsNotNone(review.date)
