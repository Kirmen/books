from django.test import TestCase

from store.logic import operations

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "books.settings")

import django

django.setup()


class LogicTestCase(TestCase):
    def test_plus(self):
        result = operations(6, 13, '+')
        self.assertEqual(19, result)

    def test_minus(self):
        result = operations(6, 13, '-')
        self.assertEqual(-7, result)

    def test_multiply(self):
        result = operations(13, 6, '*')
        self.assertEqual(78, result)
