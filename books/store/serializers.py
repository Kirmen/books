from rest_framework.serializers import ModelSerializer, SerializerMethodField, IntegerField, DecimalField

from store.models import Book, UserBookRelation


class BooksSerializer(ModelSerializer):
    likes_count = SerializerMethodField()
    annotated_likes = IntegerField(read_only=True)
    rating = DecimalField(max_digits=3, decimal_places=2, read_only=True)

    class Meta:
        model = Book
        fields = ('id', 'name', 'price', 'author', 'likes_count', 'annotated_likes', 'rating')

    def get_likes_count(self, instance):
        return UserBookRelation.objects.filter(book=instance, like=True).count()


class UserBookRelationSerializer(ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ('book', 'like', 'in_bookmarks', 'rate')
