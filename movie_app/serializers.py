from rest_framework import serializers
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

