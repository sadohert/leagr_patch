# -*- coding: utf-8 -*-
from django.db.models import permalink, signals
from google.appengine.ext import db
from ragendja.dbutils import cleanup_relations

class League(db.Model):
    """A League is a collection of divisions, which are composed of a collection of games"""
    name = db.StringProperty(required=True)
    # relook at this... may want the admins to come by way of a "_set"
    # mechanism administrators = db.ListProperty(db.Key, required=True)
    def __unicode__(self):
        return '%s' % (self.name)

    @permalink
    def get_absolute_url(self):
        return('leagrapp.view.league_standings', (), {'key': self.key()})

class Division(db.Model):
    """Defines a division, that could be made up of a number of seasons."""
    title = db.StringProperty(verbose_name='Division Title', 
        required=True, multiline=False)
    league = db.ReferenceProperty(League, required=True)

    def __unicode__(self):
        return 'Division %s' % self.title

    @permalink
    def get_absolute_url(self):
        return('leagrapp.views.current_schedule', (), {'key': self.current_season})

class Season(db.Model):
    """Defines a specific collection of games in the schedule for a division."""
    division = db.ReferenceProperty(Division, required=True)
    year = db.IntegerProperty()

    def __unicode__(self):
        return '%s (%d)' % (self.division.title, self.year)

    @permalink
    def get_absolute_url(self):
        return('leagrapp.views.current_schedule', (), {'key': self.key()})

class Team(db.Model):
    """Team within a league."""
    name = db.StringProperty(required=True)
    #club = db.StringProperty(required=False)
    #captain = db.ReferenceProperty(required=True, collection_name='captained_team_set')
    division = db.ReferenceProperty(collection_name='division_team_set')

    def __unicode__(self):
        return '%s' % self.name

    @permalink
    def get_absolute_url(self):
        return ('leagrapp.views.show_team', (), {'key': self.key()})

class Game(db.Model):
    """Date related to an actual game (yet to be) played."""
    #season = db.ReferenceProperty(Season, required=True)
    division = db.ReferenceProperty(Division, required=True)
    date = db.DateTimeProperty()
    home = db.ReferenceProperty(Team, required=True, collection_name='home_games')
    away = db.ReferenceProperty(Team, required=True, collection_name='away_games')
    game_completed = db.BooleanProperty()
    home_score = db.IntegerProperty()
    away_score = db.IntegerProperty()
    #gameID? @todo

    def __unicode__(self):
        if self.game_completed:
            return '%s at %s (%s): %d - %d' %(self.home, self.away, self.date.date(),
                self.home_score, self.away_score)
        else:
            return '%s at %s (%s): game not played' %(self.home, self.away, self.date.date())

        @permalink
        def get_absolute_url(self):
            return('leagrapp.views.game_result', (), {'key': self.key()})

class Player(db.Model):
    """Basic user profile with personal details."""
    first_name = db.StringProperty(required=True)
    last_name = db.StringProperty(required=True)
    team = db.ReferenceProperty(Team)

    def __unicode__(self):
        return '%s %s' % (self.first_name, self.last_name)

    @permalink
    def get_absolute_url(self):
        return ('leagrapp.views.player_profile', (), {'key': self.key()})

# @todo where should this next line really be?
#signals.pre_delete.connect(cleanup_relations, sender=Person)
class GameReport(db.Model):
    """A single report on the score for a game"""
    game = db.ReferenceProperty(Game, required=True)
    reporter = db.ReferenceProperty(Player, required=True)
    home_score = db.IntegerProperty()
    away_score = db.IntegerProperty()

    def __unicode__(self):
        return '%s at %s (%s): %d - %d by %s' %(self.game.home, self.game.away, 
            self.game.date.date(), self.home_score, self.away_score,self.reporter)

    @permalink
    def get_absolute_url(self):
        return('leagrapp.views.game_result', (), {'key': self.game})



