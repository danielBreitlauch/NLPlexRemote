"""
python -m unittest discover -v
"""
from plexapi.server import PlexServer

import mock
from tests.mockedRemote import MockedRemote


class CommandTestCase(MockedRemote):

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
