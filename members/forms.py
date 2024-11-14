from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)
    

class RegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields = ['username','email','password1','password2'] 

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'header_image', 'biography']

from django import forms
from .models import ReviewsFixed

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