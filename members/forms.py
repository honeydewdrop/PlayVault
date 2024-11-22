from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *

class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)
    

class RegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields = ['username','email','password1','password2'] 

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']

class HeaderImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['header_image']

class BiographyForm(forms.ModelForm):
    class Meta:
        model = UpdateProfile
        fields = "__all__"

class ReviewsFixedForm(forms.ModelForm):
    class Meta:
        model = ReviewsFixed
        fields = ['reviewtext', 'rating']  # Ensure 'user' is not included here as it is set in the view

        labels = {
            'reviewtext': 'Review Text',
            'rating': 'Rating (1-5)',
        }
        widgets = {
            'reviewtext': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
        }

class StatusForm(forms.ModelForm):
    class Meta:
        model = GameStatus
        fields = ['status']