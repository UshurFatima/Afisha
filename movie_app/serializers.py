from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from . import models
 

class ReviewSerializer(serializers.ModelSerializer):
    movie_name = serializers.SerializerMethodField()

    class Meta:
        model = models.Review
        fields = 'movie_name text stars'.split()

    def get_movie_name(self, review):
        return review.movie.title if review.movie else None


class MovieSerializer(serializers.ModelSerializer):
    director_name = serializers.SerializerMethodField()

    class Meta:
        model = models.Movie
        fields = 'id title director_name description'.split()

    def get_director_name(self, movie):
        return movie.director.name if movie.director else None


class MovieReviewSerializer(serializers.ModelSerializer):
    director_name = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = models.Movie
        fields = 'id title director_name reviews rating'.split()

    def get_director_name(self, movie):
        return movie.director.name if movie.director else None

    def get_rating(self, movie):
        reviews = movie.reviews.all()
        reviews_list = [review.stars for review in reviews]
        return sum(reviews_list)/len(reviews) if reviews else None


class DirectorSerializer(serializers.ModelSerializer):
    movies_count = serializers.SerializerMethodField()

    class Meta:
        model = models.Director
        fields = 'id name movies_count'.split()

    def get_movies_count(self, director):
        return director.movie_director.count()


class MovieValidateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=2, max_length=255)
    description = serializers.CharField()
    duration = serializers.CharField(max_length=10)
    director_id = serializers.IntegerField(min_value=1)

    def validate_director_id(self, director_id):
        try:
            models.Director.objects.get(id=director_id)
        except models.Director.DoesNotExist:
            raise ValidationError('There is no such director!')
        return director_id


class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=350)
    stars = serializers.IntegerField(min_value=1, max_value=5)
    movie_id = serializers.IntegerField(min_value=1)

    def validate_movie_id(self, movie_id):
        try:
            models.Movie.objects.get(id=movie_id)
        except models.Movie.DoesNotExist:
            raise ValidationError('Movie is not in the list!')

        return movie_id


class DirectorValidateSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=5, max_length=200)
