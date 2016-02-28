import unittest
from NLPlexRemote import English


class EnglishRegExTestCase(unittest.TestCase):

    def setUp(self):
        self.lang = English()

    def tearDown(self):
        self.lang = None

    def findMatchingKeys(self, text, assert_keys):
        for priority, command in self.lang.match(text):
            missing = [item for item in assert_keys if item not in command.keys()]
            if not missing:
                return
        # Readable error
        error = ''
        for priority, command in self.lang.match(text):
            missing = [item for item in assert_keys if item not in command.keys()]
            error += str(missing) + ' not found in: ' + str(command) + '\n'
        self.assertTrue(False, error)

    def findMatchingValues(self, text, assertions):
        for priority, command in self.lang.match(text):
            missing = [item for item in assertions.keys()
                       if item not in command.keys() or assertions[item] and assertions[item] != command[item]]
            if not missing:
                return
        # Readable error
        error = ''
        for priority, command in self.lang.match(text):
            missing = [item for item in assertions.keys() if item not in command.keys()]
            if missing:
                error += str(missing) + ' not found in: ' + str(command) + '\n'
            else:
                not_equal = [item for item in assertions.keys() if assertions[item] and assertions[item] != command[item]]
                if not_equal:
                    error += str(not_equal) + ' matched wrong: ' + str(command) + '\n'
        self.assertTrue(False, error)

    def test_go_home(self):
        self.findMatchingKeys('go home', ['main_menu'])
        self.findMatchingKeys('go to menu', ['main_menu'])

    def test_pause(self):
        self.findMatchingKeys('pause movie', ['pause_toggle'])
        self.findMatchingKeys('pause episode', ['pause_toggle'])
        self.findMatchingKeys('pause', ['pause_toggle'])

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

    def test_general_search(self):
        self.findMatchingValues('go to where were we?', {'navigate': None, 'title': 'where were we?'})
        self.findMatchingValues('play a fistful of datas', {'play': None, 'title': 'fistful of datas'})

    def test_episode(self):
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
