from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.db import models
from django.contrib.auth.models import User

from django.db import models

class Game(models.Model):
    igdb_id = models.IntegerField(unique=True)
    name = models.TextField()  # Changed to TextField
    cover_url = models.TextField(null=True, blank=True)  # Changed to TextField
    genre = models.TextField(null=True, blank=True)
    platforms = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class GamesTest(models.Model):
    igdb_id = models.IntegerField(unique=True)
    name = models.TextField()  # Changed to TextField
    cover_url = models.TextField(null=True, blank=True)  # Changed to TextField
    genre = models.TextField(null=True, blank=True)
    platforms = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    biography = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'