from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', views.logout_view, name='logout'),
    path('register/', views.sign_up, name='register'),
    path('', views.home, name='home'),
    path('profile_view/', views.profile_view, name='profile_view'),
    path('games/', views.game_list, name='game_list'),
    path("game/<int:game_id>/", views.game_detail, name='game_detail'),
    path('search/', views.search_games, name='search'),
    path('submit_review/', views.submit_review, name='submit_review'),
    path('progress_view/', views.progress_view, name='progress_view'),
    path('test/', views.test_view, name='test_view'),
    path('games/<int:game_id>/reviews/all/', views.get_all_reviews, name='get_all_reviews'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)