from django.test import TestCase

from store.models import Book
from store.serializers import BooksSerializer


class BooksSerializerTestCase(TestCase):
    def test_ok(self):
        book1 = Book.objects.create(name='Test book one', price=200.00)
        book2 = Book.objects.create(name='Test book two', price=220.00)

        data = BooksSerializer([book1, book2], many=True).data
        expected_data = [
            {
                'id': book1.id,
                'name': 'Test book one',
                'price': '200.00'
            },
            {
                'id': book2.id,
                'name': 'Test book two',
                'price': '220.00'
            }
        ]
        self.assertEqual(data, expected_data)
