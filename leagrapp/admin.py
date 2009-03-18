from django.contrib import admin
from leagrapp.models import League, Division, Team, Game

class TeamsInline(admin.TabularInline):
    model = Team

class GamesInline(admin.TabularInline):
    model = Game

class DivisionAdmin(admin.ModelAdmin):
    inlines = (TeamsInline, GamesInline)
    list_display = ('title', 'league')

admin.site.register(Division, DivisionAdmin)
