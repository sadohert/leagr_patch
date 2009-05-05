import django.test
from leagrapp.models import Team, Game, Division, League

# Create League
def createLeague(name='testleague'):
    """ Creates a test league with the given name and returns the \
    pk for the created league"""
    league = League(name=name)
    league.put()
    return league

def createDivision(name, league):
    """ Creates a test division within the given league. \
    Returns the pk for the created division."""
    division = Division(title=name, league=league)
    division.put()
    return division
    
## League Specific Tests
#class TeamTestCase(unittest.TestCase):django.test.TestCase
class LeagueTestCase(django.test.TestCase):
    def setUp(self):
        self.team_list = ['Giraffe', 'Dogs', 'Cats', 'Frogs', 'Birds', 'Lions']
        self.league_name = "testleague"

        self.league = createLeague(name=self.league_name)
        self.division_name = "premier"
        self.division = createDivision(self.division_name, self.league)

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
        self.division = createDivision(self.division_name, self.league)

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

