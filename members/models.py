from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.db import models
from django.contrib.auth.models import User

from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Company(models.Model):
    name = models.CharField(max_length=10000, blank=True, null=True)  # Changed to CharField with max_length
    description = models.TextField(blank=True, null=True)
    country = models.IntegerField(blank=True, null=True)  # ISO 3166-1 country code
    logo = models.URLField(blank=True, null=True)  # URL for the company logo
    url = models.URLField(blank=True, null=True)  # Official website URL
    created_at = models.DateTimeField(blank=True, null=True)  # Date added to IGDB
    updated_at = models.DateTimeField(blank=True, null=True)  # Last updated date
    slug = models.SlugField(max_length=10000, unique=True)  # Ensure slug has a max_length

    def __str__(self):
        return self.name if self.name else "Unnamed Company"
    
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
    companies = models.ManyToManyField(Company, blank=True)  # Change to ManyToManyField
    age_ratings = models.JSONField(default=list, blank=True)
    screenshots = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.name
    
class Screenshot(models.Model):
    game = models.ForeignKey(Game, related_name='game_screenshots', on_delete=models.CASCADE)  # Change related_name here
    url = models.URLField()  # URL of the screenshot
    height = models.IntegerField(null=True, blank=True)  # Height of the image
    width = models.IntegerField(null=True, blank=True)  # Width of the image
    image_id = models.CharField(max_length=255, unique=True)  # ID of the image

    def __str__(self):
        return f"{self.game.name} Screenshot"
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    biography = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'