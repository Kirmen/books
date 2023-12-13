from django.contrib.auth.models import User
from django.test import TestCase

from store.logic import set_rating

import os

from store.models import UserBookRelation, Book

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "books.settings")

import django

django.setup()


class SetRatingTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create(username='test_username1', first_name='Mykola', last_name='Dosh')
        user2 = User.objects.create(username='test_username2', first_name='Kyrylo', last_name='Kharkiv')
        user3 = User.objects.create(username='test_username3', first_name='Vlada', last_name='Voron')

        self.book1 = Book.objects.create(name='Test book one', price=200.00, author='Testenko Test', owner=user1)

        UserBookRelation.objects.create(user=user1, book=self.book1, like=True, rate=5)
        UserBookRelation.objects.create(user=user2, book=self.book1, like=True, rate=5)
        UserBookRelation.objects.create(user=user3, book=self.book1, like=True, rate=4)



    def test_ok(self):
        set_rating(self.book1)
        self.book1.refresh_from_db()
        self.assertEqual('4.67', str(self.book1.rating))