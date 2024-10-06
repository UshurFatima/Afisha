from django.db import models


class Director(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.CharField(max_length=50)
    director = models.ForeignKey(Director, on_delete=models.RESTRICT, related_name='movie_director')

    def __str__(self):
        return f'{self.title} - {self.director}'


class Review(models.Model):
    text = models.TextField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='review')

    def __str__(self):
        return f'{self.movie} - {self.text}'
