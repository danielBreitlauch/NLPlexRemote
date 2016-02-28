"""
python -m unittest discover -v
"""
from plexapi.library import MovieSection, ShowSection
from plexapi.server import PlexServer
from NLPlexRemote import Remote, English

import mock
import unittest


class EnglishTestCase(unittest.TestCase):

    @mock.patch.object(PlexServer, '_connect')
    @mock.patch.object(PlexServer, 'library')
    @mock.patch.object(PlexServer, 'client')
    def setUp(self, mock_client, mock_library, mock_connect):
        self.movieSection = mock.create_autospec(MovieSection)
        self.movieSection.TYPE = 'movie'
        self.showSection = mock.create_autospec(ShowSection)
        self.showSection.TYPE = 'show'
        mock_library.sections.return_value = [self.movieSection, self.showSection]

        self.remote = Remote(English(), 'http://address:32400', 'Swordmaster')

    def tearDown(self):
        self.client = None
        self.movieSection = None
        self.showSection = None
        self.remote = None

    @mock.patch.object(PlexServer, 'search')
    def test_go_home(self, mock_search):
        self.remote.execute('go home')
        self.assertTrue(self.remote.client.stop.called)

    @mock.patch.object(PlexServer, 'search')
    def test_pause(self, mock_search):
        self.remote.execute('pause movie')
        self.assertTrue(self.remote.client.pause.called)

    @mock.patch.object(PlexServer, 'search')
    def test_change_language(self, mock_search):
        self.remote.execute('change language')
        self.assertTrue(self.remote.client.switch_language.called)

    @mock.patch.object(PlexServer, 'search')
    def test_change_subtitles(self, mock_search):
        self.remote.execute('change subtitles')
        self.assertTrue(self.remote.client.subtitle.called)
        self.remote.client.subtitle.assert_called_with('next')

    @mock.patch.object(PlexServer, 'search')
    def test_subtitles_on(self, mock_search):
        self.remote.execute('turn subtitles on')
        self.assertTrue(self.remote.client.subtitle.called)
        self.remote.client.subtitle.assert_called_with('on')

    @mock.patch.object(PlexServer, 'search')
    def test_subtitles_off(self, mock_search):
        self.remote.execute('turn subtitles off')
        self.assertTrue(self.remote.client.subtitle.called)
        self.remote.client.subtitle.assert_called_with('off')

    @mock.patch.object(PlexServer, 'search')
    def test_osd(self, mock_search):
        self.remote.execute('osd')
        self.assertTrue(self.remote.client.toggleOSD.called)

    @mock.patch.object(PlexServer, 'search')
    def test_forward(self, mock_search):
        self.remote.execute('forward')
        self.assertTrue(self.remote.client.stepForward.called)

    @mock.patch.object(PlexServer, 'search')
    def test_backward(self, mock_search):
        self.remote.execute('backward')
        self.assertTrue(self.remote.client.stepBack.called)






#        if 'another_one' in self.found_actions:
#            self.last_picked = self.pick_another_one()
#            self.client.navigate(self.last_picked)
#        if 'play_it' in self.found_actions:
#           self.client.playMedia(self.last_picked)





'''
exit(0)

r.execute('play episode of how i met your mother')
r.execute('go to any movie from the 60s')
r.execute('go to any unseen movie from 2010')
r.execute('go to any unseen movie rated PG-13')
r.execute('go to any new movie with bruce willis')
r.execute('go to any unseen movie with a rating higher than 8')
r.execute('go to a fistful of datas')
r.execute('go to any episode of how i met your mother from season 4')
r.execute('go to the newest episode of how mother in season 3')
r.execute('go to any unseen episode from limitless')
r.execute('go to a new episode from agent carter')
r.execute('go to an unseen romance')
r.execute('go to an unseen action movie')
r.execute('go to any new romance with george')
r.execute('go to any unseen action movie rated PG-13')
r.execute('go to any unseen action movie with a rating higher than 4')
r.execute('play newest episode with amy acker')

r.execute('go to any episode from 88')
r.execute('filter any episode with patrick')
r.execute('another one')
r.execute('play it')

r.execute('go to any movie with alan from the 2010s')

'''
