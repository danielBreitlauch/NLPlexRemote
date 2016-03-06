
from abc import ABCMeta, abstractmethod


class Language:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.title = '(?P<title>.+?)'
        self.actor = '(?P<actor>.+)'
        self.season = '(?P<season>.+)'
        self.director = '(?P<director>.+)'
        self.higher_than_rating = '(?P<higher_rating>.+)'
        self.lower_than_rating = '(?P<lower_rating>.+)'
        self.contentRating = '(?P<contentRating>.+)'
        self.year = '(?P<year>(19|20)?(\d\d))( |$)'
        self.decade = '(?P<decade>(19|20)?\d\d)'
        self.genre = '(?P<genre>.+?)'
        self.compiled_regex = self.regular_expressions()

    @abstractmethod
    def regular_expressions(self):
        return []

    @abstractmethod
    def and_phrase(self):
        return ''
        # movie with bruce willis and alan rickman

    @abstractmethod
    def or_phrase(self):
        return ''
        # action or comedy movie

    @abstractmethod
    def decade_plural_phrase(self):
        return ''
        # movie from the 90s
        # film aus den 90ern

    def match(self, text):
        solutions = []
        for priority, reg in self.compiled_regex:
            m = reg.match(text)
            if m:
                d = dict((k, v) for k, v in m.groupdict().iteritems() if v)
                solutions.append((priority, d))
        return solutions

    @staticmethod
    def group(group, text):
        return '(?P<' + group + '>' + text + ')'

    # Navigation
    def indicate_main_menu(self, text):
        return self.group('main_menu', text)

    def indicate_subtitle_on(self, text):
        return self.group('subtitle_on', text)

    def indicate_subtitle_off(self, text):
        return self.group('subtitle_off', text)

    def indicate_subtitle_toggle(self, text):
        return self.group('subtitle_toggle', text)

    def indicate_language_toggle(self, text):
        return self.group('language_toggle', text)

    def indicate_on_screen_display(self, text):
        return self.group('osd', text)

    def indicate_jump_forward(self, text):
        return self.group('jump_forward', text)

    def indicate_jump_backward(self, text):
        return self.group('jump_backward', text)

    def indicate_pause(self, text):
        return self.group('pause', text)

    def indicate_play_after_pause(self, text):
        return self.group('play_after_pause', text)

    # play media selected
    def indicate_play(self, text):
        return self.group('play', text)

    # navigate to media selection
    def indicate_navigation(self, text):
        return self.group('navigate', text)

    # media selection
    def indicate_movie(self, text):
        return self.group('movie', text)

    def indicate_tv(self, text):
        return self.group('tv', text)

    def indicate_newest(self, text):
        return self.group('newest', text)

    def indicate_oldest(self, text):
        return self.group('oldest', text)

    def indicate_unseen(self, text):
        return self.group('unseen', text)

    # context sensitive media selection refinement
    def indicate_follow_up(self, text):
        return self.group('follow_up', text)

    def indicate_another_choice(self, text):
        return self.group('another_one', text)

    def indicate_play_it(self, text):
        return self.group('play_it', text)
