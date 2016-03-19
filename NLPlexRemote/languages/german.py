# coding=utf-8

from NLPlexRemote import Language
import re


class German(Language):

    def or_phrase(self):
        return ' oder '

    def and_phrase(self):
        return ' und '

    def decade_plural_phrase(self):
        return 'er'

    def regular_expressions(self):
        von = ' (vo(n|m)|aus) '
        vllvon = '( vo(n|m)| aus)? '
        eine = ' (eine?(n|r)? )?'
        einem = ' (eine?(m|r)?)?'

        navi = self.indicate_navigation('zeige')
        play = self.indicate_play('(spiele?|starte?)')
        follow_up = self.indicate_follow_up('(begrenze auf|filter( nach))')
        cmd = '(' + navi + '|' + play + '|' + follow_up + ')' + eine
        ab = '( ab| an)?$'

        newest = self.indicate_newest('(den|die) neue?sten? ')
        unseen = self.indicate_unseen('(ungesehenen?|neuen?) ')
        newest_unseen = '(' + newest + '|' + unseen + ')?'

        genre_movie = self.indicate_movie('(filme?|' + self.genre + '( filme?)?)')
        episode = self.indicate_tv('(episoden?|serien?)')

        time = '((dem )?(jahre? )?' + self.year + '|((der )?(dekade )?|den )' + self.decade + '(ern?)?)'

        return [
            # Navigation
            (80, re.compile(self.indicate_subtitle_on('(mache? |schalte? )?(die )?untertitel (an|ein)'), re.I)),
            (80, re.compile(self.indicate_subtitle_off('(mache? |schalte? )?(die )?untertitel aus'), re.I)),
            (80, re.compile(self.indicate_subtitle_toggle('(wechsel|wechsle|andere|ändere) (die )?untertitel'), re.I)),
            (80, re.compile(self.indicate_subtitle_toggle('schalte? (die )?untertitel um'), re.I)),
            (80, re.compile(self.indicate_language_toggle('(wechsel|wechsle|andere|ändere) (die )?sprache'), re.I)),
            (80, re.compile(self.indicate_language_toggle('schalte? (die )?sprache um'), re.I)),
            (80, re.compile(self.indicate_jump_backward('(springe? |gehe? )?(\d+ sekunden? )?zurück$'), re.I)),
            (80, re.compile(self.indicate_jump_forward('(springe? |gehe? )?(\d+ sekunden? )?vor(wärts)?$'), re.I)),
            (70, re.compile(self.indicate_main_menu('^stop.*'), re.I)),
            (80, re.compile(self.indicate_main_menu('(gehe|springe|wechsel|wechsle) (ins|zum) (haupt)?(menu|menü)'), re.I)),
            (80, re.compile(self.indicate_pause('^pause$'), re.I)),
            (80, re.compile(self.indicate_play_after_pause('^weiter$'), re.I)),
            (80, re.compile(self.indicate_play_it('spiele? ((den )?film |(die )?episode |es )?ab$'), re.I)),
            (80, re.compile(self.indicate_another_choice('^(wähle? |spiele? |zeige? )?(einen? )?anderen?$'), re.I)),
            # TV
            (70, re.compile(cmd + newest_unseen + episode + vllvon + self.title + von + 'staffel ' + self.season + ab, re.I)),
            (70, re.compile(cmd + newest_unseen + episode + von + 'staffel ' + self.season + von + self.title + ab, re.I)),
            (60, re.compile(cmd + newest_unseen + episode + vllvon + self.title + ab, re.I)),
            (60, re.compile(cmd + newest_unseen + episode + ' mit' + einem + self.actor + ab, re.I)),
            (30, re.compile(cmd + newest_unseen + episode + von + time + ab, re.I)),
            (20, re.compile(cmd + newest_unseen + episode + ' mit' + einem + self.actor + von + time + ab, re.I)),
            (30, re.compile(cmd + newest_unseen + episode + vllvon + self.title + von + time + ab, re.I)),
            (20, re.compile(cmd + newest_unseen + episode + ab, re.I)),
            # Movies:
            (50, re.compile(cmd + newest_unseen + genre_movie + ' mit' + einem + self.actor + ab, re.I)),
            (30, re.compile(cmd + newest_unseen + genre_movie + von + time + ab, re.I)),
            (20, re.compile(cmd + newest_unseen + genre_movie + ' mit' + einem + self.actor + von + time + ab, re.I)),
            (20, re.compile(cmd + newest_unseen + genre_movie + ab, re.I)),
            # General search:
            (10, re.compile(cmd + self.title + ab, re.I))
        ]
