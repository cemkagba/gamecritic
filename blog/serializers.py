from rest_framework import serializers
from .models import Game, Post, Genre
from django.contrib.auth.models import User


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name', 'slug']


class GameSerializer(serializers.ModelSerializer):
    average_rating = serializers.FloatField()
    genres = GenreSerializer(many=True, read_only=True)
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = [
            'id', 'title', 'slug', 'description', 'image', 'video',
            'genres', 'is_home', 'average_rating', 'reviews', ]

    def get_reviews(self, obj):
        return [post.title for post in obj.posts.all()]


class PostSerializer(serializers.ModelSerializer):
    game = serializers.PrimaryKeyRelatedField(queryset=Game.objects.all())
    creator = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'rating', 'description', 'creator']
