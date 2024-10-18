from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('login/', views.login_view, name='login'),
    # path('logout/', views.sign_out, name='logout'),
    path('register/', views.sign_up, name='register'),
    path('', views.home, name='home'),
    path('profile/', views.profile_view, name='profile'),
    path('games/', views.game_list, name='game_list'),
    path("game/<int:game_id>/", views.game_detail, name='game_detail'),
    path('search/', views.search_games, name='search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)