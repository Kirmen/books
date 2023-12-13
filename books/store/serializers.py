from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer, SerializerMethodField, IntegerField, DecimalField, CharField

from store.models import Book, UserBookRelation


class BookReaderSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class BooksSerializer(ModelSerializer):
    # likes_count = SerializerMethodField()
    annotated_likes = IntegerField(read_only=True)
    rating = DecimalField(max_digits=3, decimal_places=2, read_only=True)
    owner_name = CharField(source='owner.username', default='', read_only=True)

    readers = BookReaderSerializer(many=True, read_only=True)  # ,source='readers'

    class Meta:
        model = Book
        fields = (
            'id', 'name', 'price', 'author', 'annotated_likes', 'rating', 'owner_name', 'readers')  # 'likes_count',

    # def get_likes_count(self, instance):
    #     return UserBookRelation.objects.filter(book=instance, like=True).count()


class UserBookRelationSerializer(ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ('book', 'like', 'in_bookmarks', 'rate')
