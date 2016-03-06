# coding=utf-8
from NLPlexRemote import German
from tests.regexTest import RegExTestCase


class GermanRegExTestCase(RegExTestCase):

    def setUp(self):
        self.lang = German()

    def test_go_home(self):
        self.findMatchingKeys('wechsle zum hauptmenu', ['main_menu'])
        self.findMatchingKeys('stop', ['main_menu'])

    def test_pause(self):
        self.findMatchingKeys('pause', ['pause'])

    def test_play(self):
        self.findMatchingKeys('weiter', ['play_after_pause'])

    def test_change_language(self):
        self.findMatchingKeys('andere sprache', ['language_toggle'])
        self.findMatchingKeys('ändere sprache', ['language_toggle'])
        self.findMatchingKeys('wechsel die sprache', ['language_toggle'])
        self.findMatchingKeys('schalt die sprache um', ['language_toggle'])

    def test_change_subtitles(self):
        self.findMatchingKeys('andere untertitel', ['subtitle_toggle'])
        self.findMatchingKeys('wechsel die untertitel', ['subtitle_toggle'])
        self.findMatchingKeys('schalte die untertitel um', ['subtitle_toggle'])

    def test_subtitles_on(self):
        self.findMatchingKeys('schalte die untertitel ein', ['subtitle_on'])
        self.findMatchingKeys('schalt untertitel an', ['subtitle_on'])

    def test_subtitles_off(self):
        self.findMatchingKeys('schalte untertitel aus', ['subtitle_off'])

    def test_forward(self):
        self.findMatchingKeys('spring vor', ['jump_forward'])
        self.findMatchingKeys('geh 15 sekunden vorwärts', ['jump_forward'])

    def test_backward(self):
        self.findMatchingKeys('geh zurück', ['jump_backward'])
        self.findMatchingKeys('springe 10 sekunden zurück', ['jump_backward'])

    def test_play_it(self):
        self.findMatchingKeys('spiel ab', ['play_it'])
        self.findMatchingKeys('spiel es ab', ['play_it'])
        self.findMatchingKeys('spiel den film ab', ['play_it'])
        self.findMatchingKeys('spiel die episode ab', ['play_it'])

    def test_general_search(self):
        self.findMatchingValues('zeige stirb langsam', {'navigate': None, 'title': 'stirb langsam'})
        self.findMatchingValues('starte a fistful of datas', {'play': None, 'title': 'a fistful of datas'})

    def test_episode(self):
        self.findMatchingValues('spiele eine episode how i met your mother ab',
                                {'play': None, 'tv': None, 'title': 'how i met your mother'})

        self.findMatchingValues('zeige eine episode von how i met your mother aus 2008',
                                {'navigate': None, 'tv': None, 'title': 'how i met your mother', 'year': '2008'})

        self.findMatchingValues('zeige episode how i met your mother aus staffel 4',
                                {'navigate': None, 'tv': None, 'title': 'how i met your mother', 'season': '4'})

        self.findMatchingValues('zeige die neueste episode how mother aus staffel 3',
                                {'navigate': None, 'tv': None, 'newest': None, 'title': 'how mother', 'season': '3'})

        self.findMatchingValues('starte die neuste episode mit amy acker',
                                {'play': None, 'tv': None, 'newest': None, 'actor': 'amy acker'})

        self.findMatchingValues('zeige eine ungesehene episode von limitless',
                                {'navigate': None, 'tv': None, 'unseen': None, 'title': 'limitless'})

        self.findMatchingValues('zeige eine neue episode agent carter',
                                {'navigate': None, 'tv': None, 'unseen': None, 'title': 'agent carter'})

        self.findMatchingValues('zeige eine episode aus 88',
                                {'navigate': None, 'tv': None, 'year': '88'})

        self.findMatchingValues('filter nach einer episode mit patrick',
                                {'follow_up': None, 'tv': None, 'actor': 'patrick'})

        self.findMatchingKeys('andere', ['another_one'])

    def test_movies(self):
        self.findMatchingValues('zeige einen film aus den 60ern',
                                {'navigate': None, 'movie': None, 'decade': '60'})

        self.findMatchingValues('zeige einen ungesehenen film',
                                {'navigate': None, 'movie': None, 'unseen': None})

        self.findMatchingValues('zeige einen ungesehenen film aus 2010',
                                {'navigate': None, 'movie': None, 'unseen': None, 'year': '2010'})

        self.findMatchingValues('zeige einen film mit alan aus den 2010ern',
                                {'navigate': None, 'movie': None, 'actor': 'alan', 'decade': '2010'})

        self.findMatchingValues('zeige einen neuen film mit bruce willis',
                                {'navigate': None, 'movie': None, 'unseen': None, 'actor': 'bruce willis'})

        self.findMatchingValues('zeige den neusten film mit bruce willis',
                                {'navigate': None, 'movie': None, 'newest': None, 'actor': 'bruce willis'})

        self.findMatchingValues('zeige eine ungesehene romance',
                                {'navigate': None, 'movie': None, 'unseen': None, 'genre': 'romance'})

        self.findMatchingValues('zeige einen ungesehenen action film an',
                                {'navigate': None, 'movie': None, 'unseen': None, 'genre': 'action'})

        self.findMatchingValues('zeige eine neue romance mit george',
                                {'navigate': None, 'movie': None, 'unseen': None,
                                 'genre': 'romance', 'actor': 'george'})
