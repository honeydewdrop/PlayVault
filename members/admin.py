from django.contrib import admin
from .models import Game
from django.db import connection

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'genre', 'rating')
    search_fields = ('name__icontains',)
    list_filter = ('genre', 'rating')

    def get_search_results(self, request, queryset, search_term):
        print(f"Search term: {search_term}")
        results, use_distinct = super().get_search_results(request, queryset, search_term)
        print(f"Results count: {results.count()}")
        
        # Print the SQL query
        print(f"SQL Query: {results.query}")
        
        # Print the first few results
        for game in results[:5]:
            print(f"Game: {game.name}")
        
        return results, use_distinct

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        print(f"Total games in queryset: {qs.count()}")
        return qs