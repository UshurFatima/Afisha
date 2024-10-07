from django.db import models


class Director(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.CharField(max_length=50)
    director = models.ForeignKey(Director, on_delete=models.PROTECT, related_name='movie_director')

    def __str__(self):
        return f'{self.title} - {self.director}'


STARS = (
    (1, '*'),
    (2, '* *'),
    (3, '* * *'),
    (4, '* * * *'),
    (5, '* * * * *'),
)


class Review(models.Model):
    text = models.TextField()
    stars = models.IntegerField(choices=STARS, default=5)
    movie = models.ForeignKey(Movie, on_delete=models.PROTECT, null=True, related_name='reviews')

    def __str__(self):
        return self.text
