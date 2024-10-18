# Generated by Django 5.1.1 on 2024-10-18 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_game'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='genre',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='platforms',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='rating',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='release_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
