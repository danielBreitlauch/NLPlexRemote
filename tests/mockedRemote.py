"""
python -m unittest discover -v
"""
from plexapi.library import MovieSection, ShowSection
from plexapi.server import PlexServer
from NLPlexRemote import Remote, English

import mock
import unittest


class MockedRemote(unittest.TestCase):

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