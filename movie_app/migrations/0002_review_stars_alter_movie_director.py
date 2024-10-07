# Generated by Django 5.1.1 on 2024-10-07 10:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='stars',
            field=models.IntegerField(choices=[('1', '*'), ('2', '* *'), ('3', '* * *'), ('4', '* * * *'), ('5', '* * * * *')], default=5),
        ),
        migrations.AlterField(
            model_name='movie',
            name='director',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='movie_director', to='movie_app.director'),
        ),
    ]
