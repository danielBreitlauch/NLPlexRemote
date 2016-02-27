# coding=utf-8


from language import Language
from query import Query
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

        newest = self.indicate_newest('(the )?new(est)? ')
        unseen = self.indicate_unseen('unseen ')
        newest_unseen = '(' + newest + '|' + unseen + ')?'

        time = '(the )?((year )?' + self.year + '|(decade )?' + self.decade + 's?)'

        return [
            # Navigation
            (70, re.compile(self.indicate_main_menu('^stop.*'), re.I)),
            (80, re.compile(self.indicate_main_menu('(go |goto |go to )?(dashboard|home|menu|menü|home menu)'), re.I)),
            (80, re.compile(self.indicate_jump_backward('jump back(wards?)?'), re.I)),
            (80, re.compile(self.indicate_jump_forward('jump forwards?'), re.I)),
            (80, re.compile(self.indicate_pause_toggle('pause( episode| movie)?'), re.I)),
            (80, re.compile(self.indicate_subtitle_on('(turn |switch )?subtitles? on'), re.I)),
            (80, re.compile(self.indicate_subtitle_off('(turn |switch )?subtitles? off'), re.I)),
            (80, re.compile(self.indicate_subtitle_toggle('(other |next )subtitles?'), re.I)),
            (80, re.compile(self.indicate_language_toggle('(other |next |different |switch |toggle |change )languages?'), re.I)),
            (80, re.compile(self.indicate_play_it('play( it)?'), re.I)),
            (80, re.compile(self.indicate_another_choice('(choose )?an ?other( one)?'), re.I)),
            # TV
            (70, re.compile(cmd + newest_unseen + episode + of + self.title + ofin + 'season ' + self.season, re.I)),
            (70, re.compile(cmd + newest_unseen + episode + ofin + 'season ' + self.season + of + self.title, re.I)),
            (60, re.compile(cmd + newest_unseen + episode + of + self.title, re.I)),
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
            (10, re.compile(cmd + self.title, re.I))
        ]

q = Query(English(), "http://192.168.0.30:32400", "Swordmaster")


# q.execute("go to any episode of how i met your mother from 2008")

q.execute("go to any movie with alan from the 2010s")

exit(0)

q.execute("go home")
q.execute("play episode of how i met your mother")
q.execute("go to any movie from the 60s")
q.execute("go to any unseen movie from 2010")
q.execute("go to any unseen movie rated PG-13")
q.execute("go to any new movie with bruce willis")
q.execute("go to any unseen movie with a rating higher than 8")
q.execute("go to a fistful of datas")
q.execute("go to any episode of how i met your mother from season 4")
q.execute("go to the newest episode of how mother in season 3")
q.execute("go to any unseen episode from limitless")
q.execute("go to a new episode from agent carter")
q.execute("go to an unseen romance")
q.execute("go to an unseen action movie")
q.execute("go to any new romance with george")
q.execute("go to any unseen action movie rated PG-13")
q.execute("go to any unseen action movie with a rating higher than 4")
q.execute("play newest episode with amy acker")

q.execute("go to any episode from 88")
q.execute("filter any episode with patrick")
q.execute("another one")
q.execute("play it")

q.execute("go to where were we?")

q.execute("pause movie")
q.execute("change language")
