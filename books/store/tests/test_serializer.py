from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg
from django.test import TestCase

from store.models import Book, UserBookRelation
from store.serializers import BooksSerializer


class BooksSerializerTestCase(TestCase):
    def test_ok(self):
        user1 = User.objects.create(username='test_username1', first_name='Mykola', last_name='Dosh')
        user2 = User.objects.create(username='test_username2', first_name='Kyrylo', last_name='Kharkiv')
        user3 = User.objects.create(username='test_username3', first_name='Vlada', last_name='Voron')

        book1 = Book.objects.create(name='Test book one', price=200.00, author='Testenko Test', owner=user1)
        book2 = Book.objects.create(name='Test book two', price=220.00, author='Testenchuk Test')

        UserBookRelation.objects.create(user=user1, book=book1, like=True, rate=5)
        UserBookRelation.objects.create(user=user2, book=book1, like=True, rate=5)
        user_book3 = UserBookRelation.objects.create(user=user3, book=book1, like=True)
        user_book3.rate = 4
        user_book3.save()

        UserBookRelation.objects.create(user=user1, book=book2, like=True, rate=4)
        UserBookRelation.objects.create(user=user2, book=book2, like=False, rate=3)
        UserBookRelation.objects.create(user=user3, book=book2, like=True)

        books = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1)))
        ).order_by('id')  # ,rating=Avg('userbookrelation__rate')
        data = BooksSerializer(books, many=True).data
        expected_data = [
            {
                'id': book1.id,
                'name': 'Test book one',
                'price': '200.00',
                'author': 'Testenko Test',
                'annotated_likes': 3,
                'rating': '4.67',
                'owner_name': 'test_username1',
                'readers': [{'first_name': 'Mykola', 'last_name': 'Dosh'},
                            {'first_name': 'Kyrylo', 'last_name': 'Kharkiv'},
                            {'first_name': 'Vlada', 'last_name': 'Voron'}]
            },
            {
                'id': book2.id,
                'name': 'Test book two',
                'price': '220.00',
                'author': 'Testenchuk Test',

                'annotated_likes': 2,
                'rating': '3.50',
                'owner_name': '',
                'readers': [{'first_name': 'Mykola', 'last_name': 'Dosh'},
                            {'first_name': 'Kyrylo', 'last_name': 'Kharkiv'},
                            {'first_name': 'Vlada', 'last_name': 'Voron'}]
            }
        ]
        # print(data)
        # print(expected_data)
        self.assertEqual(data, expected_data)
