from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from . import models
from . import serializers
from rest_framework.permissions import IsAuthenticated


@api_view(http_method_names=['GET'])
def movie_review_list_api_view(request):
    movies = models.Movie.objects.all()
    data = serializers.MovieReviewSerializer(instance=movies, many=True).data
    return Response(data=data)


@api_view(http_method_names=['GET', 'POST'])
@permission_classes([IsAuthenticated])
def movie_list_create_api_view(request):
    print(request.user)
    if request.method == 'GET':
        movies = models.Movie.objects.all()
        data = serializers.MovieSerializer(instance=movies, many=True).data

        return Response(data=data)

    elif request.method == 'POST':
        serializer = serializers.MovieValidateSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=False):
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                            data=serializer.errors)

        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        duration = serializer.validated_data.get('duration')
        director_id = serializer.validated_data.get('director_id')

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
        serializer = serializers.MovieValidateSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=False):
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                            data=serializer.errors)

        movies.title = serializer.validated_data.get('title')
        movies.description = serializer.validated_data.get('description')
        movies.duration = serializer.validated_data.get('duration')
        movies.director_id = serializer.validated_data.get('director_id')
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
        serializer = serializers.DirectorValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        name = serializer.validated_data.get('name')
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
        serializer = serializers.DirectorValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

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
        serializer = serializers.ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        text = serializer.validated_data.get('text')
        stars = serializer.validated_data.get('stars')
        movie_id = serializer.validated_data.get('movie_id')

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
        serializer = serializers.ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        reviews.text = serializer.validated_data.get('text')
        reviews.stars = serializer.validated_data.get('stars')
        reviews.movie_id = serializer.validated_data.get('movie_id')
        reviews.save()

        return Response(data=serializers.ReviewSerializer(reviews).data,
                        status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        reviews.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

