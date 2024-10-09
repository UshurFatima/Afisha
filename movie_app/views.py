from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import models
from . import serializers
from rest_framework import status


@api_view(http_method_names=['GET'])
def movie_review_list_api_view(request):
    movies = models.Movie.objects.all()
    data = serializers.MovieReviewSerializer(instance=movies, many=True).data
    return Response(data=data)


@api_view(http_method_names=['GET', 'POST'])
def movie_list_create_api_view(request):
    if request.method == 'GET':
        movies = models.Movie.objects.all()
        data = serializers.MovieSerializer(instance=movies, many=True).data

        return Response(data=data)

    elif request.method == 'POST':
        title = request.data.get('title')
        description = request.data.get('description')
        duration = request.data.get('duration')
        director_id = request.data.get('director_id')

        movie = models.Movie.objects.create(
            title=title,
            description=description,
            duration=duration,
            director_id=director_id
        )

        return Response(status=status.HTTP_201_CREATED,
                        data={'movie_id': movie.id})


@api_view(http_method_names=['GET', 'PUT', 'DELETE'])
def movie_detail_api_view(request, id):
    try:
        movies = models.Movie.objects.get(id=id)
    except models.Movie.DoesNotExist:
        return Response(data={'error': 'Movie not found'},
                        status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        data = serializers.MovieSerializer(instance=movies, many=False).data
        return Response(data=data)

    elif request.method == 'PUT':
        movies.title = request.data.get('title')
        movies.description = request.data.get('description')
        movies.duration = request.data.get('duration')
        movies.director_id = request.data.get('director_id')
        movies.save()

        return Response(data=serializers.MovieSerializer(movies).data,
                        status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        movies.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(http_method_names=['GET', 'POST'])
def director_list_create_api_view(request):
    if request.method == 'GET':
        directors = models.Director.objects.all()
        data = serializers.DirectorSerializer(instance=directors, many=True).data

        return Response(data=data)

    elif request.method == 'POST':
        name = request.data.get('name')
        director = models.Director.objects.create(
            name=name,
        )
        return Response(status=status.HTTP_201_CREATED,
                        data={'director_id': director.id})


@api_view(http_method_names=['GET', 'PUT', 'DELETE'])
def director_detail_api_view(request, id):
    try:
        directors = models.Director.objects.get(id=id)
    except models.Director.DoesNotExist:
        return Response(data={'error': 'Director not found'},
                        status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        data = serializers.DirectorSerializer(instance=directors, many=False).data
        return Response(data=data)

    elif request.method == 'PUT':
        directors.name = request.data.get('name')
        directors.save()

        return Response(data=serializers.DirectorSerializer(directors).data,
                        status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        directors.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(http_method_names=['GET', 'POST'])
def review_list_create_api_view(request):
    if request.method == 'GET':
        review = models.Review.objects.all()
        data = serializers.ReviewSerializer(instance=review, many=True).data

        return Response(data=data)

    elif request.method == 'POST':
        text = request.data.get('text')
        stars = request.data.get('stars')
        movie_id = request.data.get('movie_id')
        review = models.Review.objects.create(
            text=text,
            stars=stars,
            movie_id=movie_id
        )
        return Response(status=status.HTTP_201_CREATED,
                        data={'review_id': review.id})


@api_view(http_method_names=['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, id):
    try:
        reviews = models.Review.objects.get(id=id)
    except models.Review.DoesNotExist:
        return Response(data={'error': 'Review not found'},
                        status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        data = serializers.ReviewSerializer(instance=reviews, many=False).data
        return Response(data=data)

    elif request.method == 'PUT':
        reviews.text = request.data.get('text')
        reviews.stars = request.data.get('stars')
        reviews.movie_id = request.data.get('movie_id')
        reviews.save()

        return Response(data=serializers.ReviewSerializer(reviews).data,
                        status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        reviews.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

