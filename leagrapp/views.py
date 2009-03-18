# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, delete_object, \
    update_object
from google.appengine.ext import db
from mimetypes import guess_type
from leagrapp.models import Team, Game, GameReport, Season, Division, \
    League, Player
from leagrapp.forms import GameEditForm
from ragendja.dbutils import get_object_or_404
from ragendja.template import render_to_response
import datetime

@login_required
def game_edit(request, league, division, game):
    return update_object(request, \
        post_save_redirect=reverse('leagrapp.views.division_main',\
        kwargs=dict(league=league, division=division)), object_id=game, form_class=GameEditForm)

def leagr_main(request):
    return render_to_response(request, 'leagrapp/leagr_mainpage.html')

def league_main(request, league):
    template_values = {'league':league}
    return render_to_response(request, 'leagrapp/league_main.html', template_values)

def sortby1(nlist, n, reverse):
    nlist[:] = [(x[n], x) for x in nlist]
    nlist.sort(reverse=reverse)
    nlist[:] = [val for (key, val) in nlist]
 
##@profileit(5)
#def sortby2(nlist ,n, reverse):
#    nlist.sort(key=operator.itemgetter(n), reverse=reverse)
#
# this should likely be localized
league_stat_categories = ["W", "L", "T", "GF", "GA", "+/-", "P"]
num_league_stats = len(league_stat_categories)

def division_main(request, league, division):
    # @todo will want to do memcached stuff here
    # when the league starts this table should be created once
    # Need to query the datastore for the key of the given division
    d = Division.all()
    #d.filter('title =', division)
    division_key = d.fetch(1)
    print division_key

    # Do a search for all the games played in the league before today,for each
    games = Game.all()
    #@todo will want this to be filtered by season and division
    games.filter('division = ', division_key[0])
    games.filter('date <=', datetime.datetime.today())
    past_games = games.fetch(20)
    # team tally winner/loser/tie and points
    standings_dict = {}

    for g in past_games:
        if g.home.name not in   standings_dict:
            standings_dict[g.home.name] = [0 for i in range(num_league_stats)]
        if g.away.name not in   standings_dict:
            standings_dict[g.away.name] = [0 for i in range(num_league_stats)]

        if g.game_completed:
        # NEED TO GET SOME results into data
            if g.home_score:
                standings_dict[g.home.name][3] += int(g.home_score)
                standings_dict[g.away.name][4] += int(g.home_score)
                if g.away_score:
                    standings_dict[g.away.name][3] += int(g.away_score)
                    standings_dict[g.home.name][4] += int(g.away_score)
                if g.home_score and g.away_score:
                    if g.home_score > g.away_score:
                        standings_dict[g.home.name][0] += 1
                        standings_dict[g.away.name][1] += 1
                    elif g.home_score < g.away_score:
                        standings_dict[g.away.name][0] += 1
                        standings_dict[g.home.name][1] += 1
                    else:
                        standings_dict[g.away.name][2] += 1
                        standings_dict[g.home.name][2] += 1

    #total point scores and calculate goal difference
    standings = []
    for t in standings_dict.keys():
        standings_dict[t][5] = standings_dict[t][3]-standings_dict[t][4]
        # 3 pts for win, 1 pt for tie
        standings_dict[t][6] = 3*standings_dict[t][0] + 1*standings_dict[t][2]
        standings.append([t] + standings_dict[t][:])
        #standings[:-1] = [t] + standings_dict[t][:]

    # Convert to tuple for sorting
    #standings = standings_dict.items()
    # Sort by Points in descending order
    #print standings
    sortby1(standings, 6, True)


    # Create upcoming game dictionary

    # Do a search for the games played in the league after today
    games = Game.all()
    #@todo will want this to be filtered by season and division
    games.filter('division = ', division_key[0])
    games.filter('date >', datetime.datetime.today())
    games.order('date')
    upcoming_games = games.fetch(len(standings_dict.keys())/2)
    # Return to a template that renders this data
    template_values = {'standings':standings, 'upcoming_games':upcoming_games, \
        'past_games':past_games}        
    template_values['league'] = league
    template_values['division'] = division


    return render_to_response(request, 'leagrapp/division.html', template_values)

def team_main(request, league, division, team):
    template_values = {}
    template_values['league'] = league
    template_values['division'] = division
    template_values['team'] = team
    return render_to_response(request, 'leagrapp/team_main.html', template_values)

#def enter_result(request, game):
#       return render_to_response(request, 'leagrapp/team_main.html', template_values)
