# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('leagrapp.views',
    (r'(?P<league>\w+)/div/(?P<division>\w+)/team/(?P<team>\w+)/$', 'team_main'),
    (r'(?P<league>\w+)/div/(?P<division>\w+)/game/(?P<game>\w+)/$', 'game_edit'),
    (r'(?P<league>\w+)/div/(?P<division>\w+)/$', 'division_main'),
    (r'(?P<league>\w+)/$', 'league_main'),
    (r'.*/$', 'leagr_main'),
		)
