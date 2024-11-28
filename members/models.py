from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
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
    
class Game(models.Model):
    igdb_id = models.IntegerField(unique=True)
    name = models.TextField()  
    cover_url = models.TextField(null=True, blank=True)  
    genre = models.TextField(null=True, blank=True)
    platforms = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    companies = models.ManyToManyField('Company', related_name='games', blank=True)  # Many-to-many relationship
    age_ratings = models.JSONField(default=list, blank=True)
    screenshots = models.JSONField(default=list, blank=True)

class Company(models.Model):
    name = models.CharField(max_length=10000, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    country = models.IntegerField(blank=True, null=True)  # ISO 3166-1 country code
    logo = models.URLField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)  
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    slug = models.SlugField(max_length=10000, unique=True)  
    
    def __str__(self):
        return self.name if self.name else "Unnamed Company"


    def __str__(self):
        return self.name

class InvolvedCompany(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='involved_companies')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    developer = models.BooleanField(default=False)
    publisher = models.BooleanField(default=False)
    porting = models.BooleanField(default=False)
    supporting = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('game', 'company')  # Ensure each game-company pair is unique

    def __str__(self):
        return f"{self.company.name} - {self.get_role_display()} for {self.game.name}"

    def get_role_display(self):
        roles = []
        if self.developer:
            roles.append('Developer')
        if self.publisher:
            roles.append('Publisher')
        if self.porting:
            roles.append('Porting')
        if self.supporting:
            roles.append('Supporting')
        return ', '.join(roles)
    
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
    header_image = models.ImageField(upload_to='header_pics/', blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'
    
class UpdateProfile(models.Model):
    biography = models.TextField(max_length=500, blank=True)
    
class ReviewsFixed(models.Model):
    game = models.ForeignKey('Game', related_name='reviews', on_delete=models.CASCADE)  # Ensure Game model is defined
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reviewtext = models.TextField()
    rating = models.PositiveSmallIntegerField(
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )  # Enforce rating range from 1 to 5
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'game')

    def __str__(self):
        return f"{self.user.username} - {self.game.name}"

class GameStatus(models.Model):
    STATUS_CHOICES = [
        ('planning', 'Planning'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user
    game = models.ForeignKey(Game, on_delete=models.CASCADE)  # Link to the game
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)  # Status of the game
    updated_at = models.DateTimeField(auto_now=True)  # Track when the status was last updated

    class Meta:
        unique_together = ('user', 'game')  # Ensure a user can only have one status per game

    def __str__(self):
        return f"{self.user.username} - {self.game.name}: {self.status}"
    
# class NewReviewsFixed(models.Model):
#        game = models.ForeignKey('Game', related_name='new_reviews', on_delete=models.CASCADE)
#        user = models.ForeignKey(User, on_delete=models.CASCADE)
#        reviewtext = models.TextField()
#        rating = models.PositiveSmallIntegerField(
#            default=1,
#            validators=[MinValueValidator(1), MaxValueValidator(5)]
#        )
#        created_at = models.DateTimeField(default=timezone.now)

#        def __str__(self):
#            return f"{self.user.username} - {self.game.name}"