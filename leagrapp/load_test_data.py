# -*- coding: utf-8 -*-
from leagrapp.models import Team, Game, Division, League
from django.contrib.auth.models import User
from copy import deepcopy
import datetime

league_name = "testleague"
division_name = "Premier"
team_list = ['Giraffe', 'Dogs', 'Cats', 'Frogs', 'Birds', 'Lions']

Nteams = len(team_list)
Ngames_per_week = Nteams/2
Nweeks = Nteams - 1
delta_weeks = -4

def rotate_pairings(pairings):
		#Start on right, move to bottom, then move up left
		new_pairings = deepcopy(pairings)
		height = len(pairings)
		x = 1
		y = 1
		delta = 1
		previous_idx = pairings[0][1]
		if height > 1:
				for i in range(2*height-1-1):
						new_pairings[y][x] = previous_idx
						previous_idx = pairings[y][x]
						y = y+delta
						if y == height:
								delta = -1
								x = 0
								y = height-1
						if x == 0 and y == 0:
								new_pairings[0][1] = previous_idx
				
		return new_pairings

# Create a league
new_league = League(name=league_name)
new_league.put()
# Create a division
new_division = Division(title=division_name, league=new_league)
new_division.put()

# Create teams in database
for t in team_list:
		print "Adding team: %s" % t
		new_team = Team(name=t, division=new_division)
		new_team.put()
# Initialize first round pairings
pairings = []
for i in range(Nteams/2):
		pairings.append([2*i, 2*i+1])

all_teams = new_division.division_team_set
# For testing purposes start the season 'delta_weeks' ago
start_delta = datetime.timedelta(delta_weeks*4)
season_start = datetime.datetime.today() + start_delta
season_start = season_start.replace(hour=19, minute=00, second=0, microsecond=0)
current_week = season_start
# Used to swap who is home and who is away
h = 0
a = 1
for i in range(Nweeks):
		# Create the matchups for the week
		for j in range(Nteams/2):
				g = Game(division=new_division, date=current_week, home=all_teams[pairings[j][h]], away=all_teams[pairings[j][a]], game_completed=False)
				g.put()

		#rotate the pairings
		pairings = rotate_pairings(pairings)
		#swap which is home and which is away
		h = not h
		a = not a
		#increment date
		current_week = current_week + datetime.timedelta(7)

print "DATA LOADED"
user = User.get_by_key_name('admin')
if not user or user.username != 'admin' or not (user.is_active and user.is_staff and user.is_superuser and user.check_password('admin')):
	user = User(key_name='admin', username='admin', email='admin@localhost', first_name='Boss', last_name='Admin', is_active=True, is_staff=True, is_superuser=True)
	user.set_password('admin')
	user.put()
print "SUPERUSER ADMIN CREATED"
