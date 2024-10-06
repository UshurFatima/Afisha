from rest_framework import serializers
from . import models


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Movie
        fields = 'id title director'.split()


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Director
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = 'text movie'.split()
