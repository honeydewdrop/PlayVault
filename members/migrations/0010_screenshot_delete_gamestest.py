# Generated by Django 5.1.1 on 2024-10-27 22:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0009_game_age_ratings_game_companies_game_screenshots'),
    ]

    operations = [
        migrations.CreateModel(
            name='Screenshot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('height', models.IntegerField(blank=True, null=True)),
                ('width', models.IntegerField(blank=True, null=True)),
                ('image_id', models.CharField(max_length=255, unique=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game_screenshots', to='members.game')),
            ],
        ),
        migrations.DeleteModel(
            name='GamesTest',
        ),
    ]
