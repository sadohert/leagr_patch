import django.test
from leagrapp.models import Team, Game, Division, League

# Create League
def createLeague(name='testleague'):
    """ Creates a test league with the given name and returns the \
    pk for the created league"""
    league = League(name=name)
    league.put()
    return league

def createDivision(name, league, num_teams, num_games, num_finished_games):
    """ Creates a test division within the given league. \
    Returns the pk for the created division."""
    division = Division(title=name, league=league)
    division.put()
    return division

def createSchedule(team_set, start_date, num_games):
    """Creates a season of games based on the input parameters"""
    pass

def createWholeLeague(name, num_divisions, num_teams, num_games, num_finished_games):    
    """ Method creates and stores all the objects relevant to a particular 
    league setup
    Inputs:
    num_divisions - Number of distinct divisions to create
    num_teams - Number of teams in each division
    num_games - Number of games played by each team in the season
    num_finished_games - Number of games that have already completed
    """
    league = createLeague(name)
    divisions = []
    
    data_set = {}
    for d in range(num_divisions):
        division_name = "Div%d_%s" % (d, league.name)
        div = createDivision(division_name, league, 0, 0, 0)
        divisions.append(div)


## League Specific Tests
#class TeamTestCase(unittest.TestCase):django.test.TestCase
class LeagueTestCase(django.test.TestCase):
    def setUp(self):
        self.team_list = ['Giraffe', 'Dogs', 'Cats', 'Frogs', 'Birds', 'Lions']
        self.league_name = "testleague"

        self.league = createLeague(name=self.league_name)
        self.division_name = "premier"
        self.division = createDivision(self.division_name, self.league, 0, 0, 0)

        # Create teams in database
        self.teams = []
        for t in self.team_list:
            #print "Adding team: %s" % t
            new_team = Team(name=t, division=self.division)
            new_team.put()
            self.teams.append(new_team)

    def testLeagueSetup(self):
        l = League.all().fetch(1)[0]
        self.assertEquals(l.pk, self.league.pk)
        self.assertEquals(l.name, self.league_name)


    #def testTeamSetups(self):
        #self.assertEquals(self.lion.speak(), 'The lion says "roar"')
        #self.assertEquals(self.cat.speak(), 'The cat says "meow"')
class DivisionTestCase(django.test.TestCase):
    def setUp(self):
        self.team_list = ['Giraffe', 'Dogs', 'Cats', 'Frogs', 'Birds', 'Lions']
        self.league_name = "testleague"
        #self.league = League(name=self.league_name)
        #self.league.put()
        self.league = createLeague(name=self.league_name)
        self.division_name = "premier"
        self.division = createDivision(self.division_name, self.league, 0, 0, 0)

        # Create teams in database
        self.teams = []
        for t in self.team_list:
            #print "Adding team: %s" % t
            new_team = Team(name=t, division=self.division)
            new_team.put()
            self.teams.append(new_team)


    def testDivisionSetup(self):
        d = Division.all().fetch(1)[0]
        self.assertEquals(len(d.division_team_set), len(self.team_list))

class GameEditTestCase(django.test.TestCase):
    def setUp(self):
        self.team_list = ['Giraffe', 'Dogs']
        self.league_name = "testleague"
        self.league = createLeague(name=self.league_name)
        self.division_name = "premier"
        self.division = createDivision(self.division_name, self.league, 0, 0, 0)

        # Create teams in database
        self.teams = []
        for t in self.team_list:
            #print "Adding team: %s" % t
            new_team = Team(name=t, division=self.division)
            new_team.put()
            self.teams.append(new_team)


        
