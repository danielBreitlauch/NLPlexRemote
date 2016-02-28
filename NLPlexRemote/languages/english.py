# coding=utf-8

from NLPlexRemote import Language
import re


class English(Language):

    def and_phrase(self):
        return ' and '

    def or_phrase(self):
        return ' or '

    def decade_plural_phrase(self):
        return 's'

    def regular_expressions(self):
        an = ' (an?y? )?'
        of = ' (of|from) '
        ofin = ' (of|from|in) '

        genre_movie = self.indicate_movie('(movies?|' + self.genre + '( movies?)?)')
        episode = self.indicate_tv('episodes?')

        navi = self.indicate_navigation('go( ?to)?')
        play = self.indicate_play('(play|put on)')
        follow_up = self.indicate_follow_up('(restrict|filter)')
        cmd = '(' + navi + '|' + play + '|' + follow_up + ')' + an

        newest = self.indicate_newest('(the )?newest ')
        unseen = self.indicate_unseen('(unseen|new) ')
        newest_unseen = '(' + newest + '|' + unseen + ')?'

        time = '(the )?((year )?' + self.year + '|(decade )?' + self.decade + 's?)'

        change = '(other |next |different |switch |toggle |change )'

        return [
            # Navigation
            (70, re.compile(self.indicate_on_screen_display('^osd$'), re.I)),
            (70, re.compile(self.indicate_main_menu('^stop.*'), re.I)),
            (80, re.compile(self.indicate_main_menu('(go |goto |go to )?(dashboard|home|menu|menü|home menu)'), re.I)),
            (80, re.compile(self.indicate_jump_backward('(jump |step )*back(wards?)?'), re.I)),
            (80, re.compile(self.indicate_jump_forward('(jump |step )*forwards?'), re.I)),
            (80, re.compile(self.indicate_pause_toggle('pause( episode| movie)?'), re.I)),
            (80, re.compile(self.indicate_subtitle_on('(turn |switch )?subtitles? on'), re.I)),
            (80, re.compile(self.indicate_subtitle_off('(turn |switch )?subtitles? off'), re.I)),
            (80, re.compile(self.indicate_subtitle_toggle(change + 'subtitles?'), re.I)),
            (80, re.compile(self.indicate_language_toggle(change + 'languages?'), re.I)),
            (80, re.compile(self.indicate_play_it('^play( it)?$'), re.I)),
            (80, re.compile(self.indicate_another_choice('(choose )?an ?other( one)?'), re.I)),
            # TV
            (70, re.compile(cmd + newest_unseen + episode + of + self.title + ofin + 'season ' + self.season, re.I)),
            (70, re.compile(cmd + newest_unseen + episode + ofin + 'season ' + self.season + of + self.title + '$', re.I)),
            (60, re.compile(cmd + newest_unseen + episode + of + self.title + '$', re.I)),
            (60, re.compile(cmd + newest_unseen + episode + ' with' + an + self.actor, re.I)),
            (30, re.compile(cmd + newest_unseen + episode + of + time, re.I)),
            (20, re.compile(cmd + newest_unseen + episode + ' with' + an + self.actor + of + time, re.I)),
            (30, re.compile(cmd + newest_unseen + episode + of + self.title + of + time, re.I)),
            # Movies:
            (50, re.compile(cmd + newest_unseen + genre_movie + ' with' + an + self.actor, re.I)),
            (40, re.compile(cmd + newest_unseen + genre_movie + of + '(the )?(director )?' + self.director, re.I)),
            (30, re.compile(cmd + newest_unseen + genre_movie + of + time, re.I)),
            (20, re.compile(cmd + newest_unseen + genre_movie + ' with' + an + self.actor + of + time, re.I)),
            (20, re.compile(cmd + newest_unseen + genre_movie + ' with( a)?( better| higher)? rating( above| better| higher| over)? (as|than|then) ' + self.higher_than_rating, re.I)),
            (20, re.compile(cmd + newest_unseen + genre_movie + ' with( a)?( worse| lower)? rating( below| worse| lower| under)? (as|than|then) ' + self.lower_than_rating, re.I)),
            (20, re.compile(cmd + newest_unseen + genre_movie + ' (with( a)? content rating( of)?| (which|who) are rated) ' + self.contentRating, re.I)),
            (20, re.compile(cmd + newest_unseen + genre_movie + ' rated ' + self.contentRating, re.I)),
            (20, re.compile(cmd + newest_unseen + genre_movie + '$', re.I)),
            (20, re.compile(cmd + self.contentRating + ' rated ' + newest_unseen + genre_movie, re.I)),
            # General search:
            (10, re.compile(cmd + self.title + '$', re.I))
        ]
