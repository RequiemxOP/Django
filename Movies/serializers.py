from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Movie, Collection


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('title', 'description', 'genres', 'uuid')


class PagedMoviesSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.URLField(required=False, allow_null=True)
    previous = serializers.URLField(required=False, allow_null=True)
    results = MovieSerializer(many=True)


class CollectionSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True, required=False)
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Collection
        fields = ['uuid', 'title', 'description', 'movies', 'user']  

    def create(self, validated_data):
        movies_data = validated_data.pop('movies', [])
        collection = Collection.objects.create(**validated_data)
        for movie_data in movies_data:
            Movie.objects.create(collection=collection, **movie_data)
        return collection

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        movies_data = validated_data.pop('movies', None)
        if movies_data is not None:
           
            Movie.objects.filter(collection=instance).delete()
            for movie_data in movies_data:
                Movie.objects.create(collection=instance, **movie_data)

        return instance
