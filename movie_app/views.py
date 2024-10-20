from collections import OrderedDict
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from . import models
from . import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('total', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data),
        ]))


class MovieReviewListAPIView(ListAPIView):
    queryset = models.Movie.objects.all()
    serializer_class = serializers.MovieReviewSerializer
    pagination_class = CustomPagination

# @api_view(http_method_names=['GET'])
# def movie_review_list_api_view(request):
#     movies = models.Movie.objects.all()
#     data = serializers.MovieReviewSerializer(instance=movies, many=True).data
#     return Response(data=data)


class MovieListCreateAPIView(ListCreateAPIView):
    queryset = models.Movie.objects.all()
    serializer_class = serializers.MovieSerializer
    pagination_class = CustomPagination

    def post(self, request, **kwargs):
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


class MovieDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = models.Movie.objects.all()
    serializer_class = serializers.MovieSerializer
    lookup_field = 'id'
    
    def update(self, request, *args, **kwargs):
        movies = self.get_object()
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


# @api_view(http_method_names=['GET', 'PUT', 'DELETE'])
# def movie_detail_api_view(request, id):
#     try:
#         movies = models.Movie.objects.get(id=id)
#     except models.Movie.DoesNotExist:
#         return Response(data={'error': 'Movie not found'},
#                         status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         data = serializers.MovieSerializer(instance=movies, many=False).data
#         return Response(data=data)
#
#     elif request.method == 'PUT':
#         serializer = serializers.MovieValidateSerializer(data=request.data)
#         if not serializer.is_valid(raise_exception=False):
#             return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
#                             data=serializer.errors)
#
#         movies.title = serializer.validated_data.get('title')
#         movies.description = serializer.validated_data.get('description')
#         movies.duration = serializer.validated_data.get('duration')
#         movies.director_id = serializer.validated_data.get('director_id')
#         movies.save()
#
#         return Response(data=serializers.MovieSerializer(movies).data,
#                         status=status.HTTP_201_CREATED)
#
#     elif request.method == 'DELETE':
#         movies.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class DirectorListCreateAPIView(ListCreateAPIView):
    queryset = models.Director.objects.all()
    serializer_class = serializers.DirectorSerializer
    pagination_class = CustomPagination

    def create(self, request, *args, **kwargs):
        serializer = serializers.DirectorValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        name = serializer.validated_data.get('name')
        director = models.Director.objects.create(
            name=name,
        )
        return Response(status=status.HTTP_201_CREATED,
                        data={'director_id': director.id})


class DirectorDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = models.Director.objects.all()
    serializer_class = serializers.DirectorSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        directors = self.get_object()
        serializer = serializers.DirectorValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        directors.name = request.data.get('name')
        directors.save()

        return Response(data=serializers.DirectorSerializer(directors).data,
                        status=status.HTTP_201_CREATED)


class ReviewListCreateAPIView(ListCreateAPIView):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    pagination_class = CustomPagination

    def create(self, request, *args, **kwargs):
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


class ReviewDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        reviews = self.get_object()
        serializer = serializers.ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        reviews.text = serializer.validated_data.get('text')
        reviews.stars = serializer.validated_data.get('stars')
        reviews.movie_id = serializer.validated_data.get('movie_id')
        reviews.save()

        return Response(data=serializers.ReviewSerializer(reviews).data,
                        status=status.HTTP_201_CREATED)
