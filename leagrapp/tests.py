import unittest
from leagrapp.models import Team, Game, Division, League

class TeamTestCase(unittest.TestCase):
    def setUp(self):
        self.team_list = ['Giraffe', 'Dogs', 'Cats', 'Frogs', 'Birds', 'Lions']
        self.league_name = "testleague"
        self.league = League(name=self.league_name)
        self.league.put()
        print "League pk is ***: %s" % self.league.pk
        self.division_name = "premier"
        self.division = Division(title=self.division_name, league=self.league)
        self.division.put()

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

    def testDivisionSetup(self):
        d = Division.all().fetch(1)[0]
        self.assertEquals(len(d.division_team_set), len(self.team_list))


    #def testTeamSetups(self):
        #self.assertEquals(self.lion.speak(), 'The lion says "roar"')
        #self.assertEquals(self.cat.speak(), 'The cat says "meow"')
