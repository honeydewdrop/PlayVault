from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    # path('logout/', views.sign_out, name='logout'),
    path('register/', views.sign_up, name='register'),
    path('', views.home, name='home'),
    path('profile/', views.profile_view, name='profile'),
]