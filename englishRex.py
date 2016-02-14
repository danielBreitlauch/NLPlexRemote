# coding=utf-8
import re

any = ' (an?y? )?'
of = ' (of|from) '

title = '(?P<title>.+)'
menu = '(?P<menu>dashboard|home|menu|menü)'
actor = '(?P<actor>.+)'
season = '(?P<season>.+)'
director = '(?P<director>.+)'
rating = '(?P<rating>.*)'
contentRating = '(?P<contentRating>.*)'

navi = '(?P<navi>go( ?to)?)'
play = '(?P<play>play)'
cmd = '(' + navi + '|' + play + ')' + any

newest = '(?P<newest>new(est)? )?'
unseen = '(?P<unseen>unseen )?'
newestUnseen = '(' + newest + '|' + unseen + ')'

year = '(year )?(?P<year>(19|20)(\d\d)?)'
decade = '(decade )?(?P<decade>(19|20)?\d\ds?)'
time = '(' + year + '|' + decade + ')'

regex = []
regex.append((80, None, re.compile(cmd + menu, re.I)))    # go to dashboard
regex.append((70, 'TV Shows', re.compile(cmd + 'episodes?' + of + title + of + 'season ' + season, re.I)))  # play (a) episode of <series> with <actor>
regex.append((60, 'TV Shows', re.compile(cmd + newestUnseen + 'episodes?' + of + title, re.I)))  # play (a) new(est) or unseen episode of <series>
regex.append((50, 'Movies', re.compile(cmd + newestUnseen + 'movie with' + any + actor, re.I)))    # play (newest, unseen) movie with <actor>
regex.append((40, 'Movies', re.compile(cmd + newestUnseen + 'movie' + of + '(the )?(director )?' + director, re.I)))  # play (newest, unseen) movie from director <director>
regex.append((30, 'Movies', re.compile(cmd + 'movies?' + of + 'the ' + time, re.I)))  # play a(ny) movie from the year or decade <year|decade>
regex.append((20, 'Movies', re.compile(cmd + 'movies? with( a)?( better)? rating( above| better)? (as|than|then) ' + rating, re.I)))  # play a(ny) movie with a rating above <rating>
regex.append((20, 'Movies', re.compile(cmd + 'movies? (with( a)? content rating( of)?| (which|who) are rated) ' + contentRating, re.I)))  # play a(ny) movie with a content rating  R
regex.append((20, 'Movies', re.compile(cmd + contentRating + ' rated movies?', re.I)))  # play a(ny) R rated movie
regex.append((10, None, re.compile(cmd + title, re.I)))   # play <title>


# content rating R
# non plex controls


def match(text):
    solutions = []
    for priority, category, reg in regex:
        m = reg.match(text)
        if m:
            d = dict((k, v) for k, v in m.groupdict().iteritems() if v)
            if category:
                d['category'] = category
            solutions.append((d, priority))
    return solutions
