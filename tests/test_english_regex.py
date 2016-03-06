from NLPlexRemote import English
from tests.regexTest import RegExTestCase


class EnglishRegExTestCase(RegExTestCase):

    def setUp(self):
        self.lang = English()

    def test_go_home(self):
        self.findMatchingKeys('go home', ['main_menu'])
        self.findMatchingKeys('go to menu', ['main_menu'])

    def test_pause(self):
        self.findMatchingKeys('pause movie', ['pause'])
        self.findMatchingKeys('pause episode', ['pause'])
        self.findMatchingKeys('pause', ['pause'])

    def test_play(self):
        self.findMatchingKeys('play', ['play_after_pause'])
        self.findMatchingKeys('play again', ['play_after_pause'])

    def test_change_language(self):
        self.findMatchingKeys('change language', ['language_toggle'])
        self.findMatchingKeys('switch language', ['language_toggle'])

    def test_change_subtitles(self):
        self.findMatchingKeys('change subtitle', ['subtitle_toggle'])
        self.findMatchingKeys('switch subtitles', ['subtitle_toggle'])

    def test_subtitles_on(self):
        self.findMatchingKeys('turn subtitles on', ['subtitle_on'])
        self.findMatchingKeys('switch subtitles on', ['subtitle_on'])

    def test_subtitles_off(self):
        self.findMatchingKeys('turn subtitles off', ['subtitle_off'])
        self.findMatchingKeys('switch subtitle off', ['subtitle_off'])

    def test_osd(self):
        self.findMatchingKeys('osd', ['osd'])

    def test_forward(self):
        self.findMatchingKeys('forward', ['jump_forward'])
        self.findMatchingKeys('forwards', ['jump_forward'])

    def test_backward(self):
        self.findMatchingKeys('backward', ['jump_backward'])
        self.findMatchingKeys('jump back', ['jump_backward'])

    def test_play_it(self):
        self.findMatchingKeys('play it', ['play_it'])
        self.findMatchingKeys('play movie', ['play_it'])
        self.findMatchingKeys('play episode', ['play_it'])

    def test_general_search(self):
        self.findMatchingValues('go to where were we?', {'navigate': None, 'title': 'where were we?'})
        self.findMatchingValues('play a fistful of datas', {'play': None, 'title': 'fistful of datas'})

    def test_episode(self):
        self.findMatchingValues('go to new episodes',
                                {'navigate': None, 'tv': None, 'unseen': None})

        self.findMatchingValues('play episode of how i met your mother',
                                {'play': None, 'tv': None, 'title': 'how i met your mother'})

        self.findMatchingValues('go to any episode of how i met your mother from 2008',
                                {'navigate': None, 'tv': None, 'title': 'how i met your mother', 'year': '2008'})

        self.findMatchingValues('goto any episode of how i met your mother from season 4',
                                {'navigate': None, 'tv': None, 'title': 'how i met your mother', 'season': '4'})

        self.findMatchingValues('go to the newest episode of how mother in season 3',
                                {'navigate': None, 'tv': None, 'newest': None, 'title': 'how mother', 'season': '3'})

        self.findMatchingValues('play newest episode with amy acker',
                                {'play': None, 'tv': None, 'newest': None, 'actor': 'amy acker'})

        self.findMatchingValues('go to any unseen episode from limitless',
                                {'navigate': None, 'tv': None, 'unseen': None, 'title': 'limitless'})

        self.findMatchingValues('go to a new episode from agent carter',
                                {'navigate': None, 'tv': None, 'unseen': None, 'title': 'agent carter'})

        self.findMatchingValues('go to any episode from 88',
                                {'navigate': None, 'tv': None, 'year': '88'})

        self.findMatchingValues('filter any episode with patrick',
                                {'follow_up': None, 'tv': None, 'actor': 'patrick'})

        self.findMatchingKeys('another one', ['another_one'])

    def test_movies(self):
        self.findMatchingValues('go to any movie from the 60s',
                                {'navigate': None, 'movie': None, 'decade': '60'})

        self.findMatchingValues('go to any unseen movie from 2010',
                                {'navigate': None, 'movie': None, 'unseen': None, 'year': '2010'})

        self.findMatchingValues('go to any movie with alan from the 2010s',
                                {'navigate': None, 'movie': None, 'actor': 'alan', 'decade': '2010'})

        self.findMatchingValues('go to any new movie with bruce willis',
                                {'navigate': None, 'movie': None, 'unseen': None, 'actor': 'bruce willis'})

        self.findMatchingValues('go to the newest movie with bruce willis',
                                {'navigate': None, 'movie': None, 'newest': None, 'actor': 'bruce willis'})

        self.findMatchingValues('go to an unseen romance',
                                {'navigate': None, 'movie': None, 'unseen': None, 'genre': 'romance'})

        self.findMatchingValues('go to an unseen action movie',
                                {'navigate': None, 'movie': None, 'unseen': None, 'genre': 'action'})

        self.findMatchingValues('go to any new romance with george',
                                {'navigate': None, 'movie': None, 'unseen': None,
                                 'genre': 'romance', 'actor': 'george'})

        self.findMatchingValues('go to any unseen movie rated PG-13',
                                {'navigate': None, 'movie': None, 'unseen': None, 'contentRating': 'PG-13'})

        self.findMatchingValues('go to any unseen action movie rated PG-13',
                                {'navigate': None, 'movie': None, 'unseen': None,
                                 'genre': 'action', 'contentRating': 'PG-13'})

        self.findMatchingValues('go to any unseen movie with a rating higher than 8',
                                {'navigate': None, 'movie': None, 'unseen': None, 'higher_rating': '8'})

        self.findMatchingValues('go to any unseen action movie with a rating lower than 4',
                                {'navigate': None, 'movie': None, 'unseen': None,
                                 'genre': 'action', 'lower_rating': '4'})
