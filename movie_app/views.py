from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import models
from . import serializers
from rest_framework import status


@api_view(http_method_names=['GET'])
def movie_list_api_view(request):
    movies = models.Movie.objects.all()
    data = serializers.MovieSerializer(instance=movies, many=True).data
    return Response(data=data)


@api_view(http_method_names=['GET'])
def movie_detail_api_view(request, id):
    try:
        movies = models.Movie.objects.get(id=id)
    except models.Movie.DoesNotExist:
        return Response(data={'error': 'Movie not found'},
                        status=status.HTTP_404_NOT_FOUND)
    data = serializers.MovieSerializer(instance=movies, many=False).data
    return Response(data=data)


@api_view(http_method_names=['GET'])
def director_list_api_view(request):
    directors = models.Director.objects.all()
    data = serializers.DirectorSerializer(instance=directors, many=True).data
    return Response(data=data)


@api_view(http_method_names=['GET'])
def director_detail_api_view(request, id):
    try:
        directors = models.Director.objects.get(id=id)
    except models.Director.DoesNotExist:
        return Response(data={'error': 'Director not found'},
                        status=status.HTTP_404_NOT_FOUND)
    data = serializers.DirectorSerializer(instance=directors, many=False).data
    return Response(data=data)


@api_view(http_method_names=['GET'])
def review_list_api_view(request):
    review = models.Review.objects.all()
    data = serializers.ReviewSerializer(instance=review, many=True).data
    return Response(data=data)


@api_view(http_method_names=['GET'])
def review_detail_api_view(request, id):
    try:
        reviews = models.Review.objects.get(id=id)
    except models.Review.DoesNotExist:
        return Response(data={'error': 'Review not found'},
                        status = status.HTTP_404_NOT_FOUND)
    data = serializers.ReviewSerializer(instance=reviews, many=False).data
    return Response(data=data)

