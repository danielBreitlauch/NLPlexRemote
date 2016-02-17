# coding=utf-8
import re

any = ' (an?y? )?'
of = ' (of|from) '
ofin = ' (of|from|in) '

title = '(?P<title>.+)'
menu = '(?P<menu>dashboard|home|menu|menü)'
actor = '(?P<actor>.+)'
season = '(?P<season>.+)'
director = '(?P<director>.+)'
higher_than_rating = '(?P<higher_rating>.+)'
lower_than_rating = '(?P<lower_rating>.+)'
contentRating = '(?P<contentRating>.+)'
genreMovie = '(movies?|(?P<genre>.+?)( movies?)?) '

navi = '(?P<navi>go( ?to)?)'
play = '(?P<play>play)'
cmd = '(' + navi + '|' + play + ')' + any

newest = '(?P<newest>(the )?new(est)?)?'
unseen = '(?P<unseen>unseen)?'
newestUnseen = '(' + newest + '|' + unseen + ') '

year = '(year )?(?P<year>(19|20)(\d\d)?)( |$)'
decade = '(decade )?(?P<decade>(19|20)?\d\ds?)'
time = '(the )?(' + year + '|' + decade + ')'

regex = []
regex.append((80, None, re.compile(cmd + menu, re.I)))    # go to dashboard
regex.append((70, 'TV Shows', re.compile(cmd + newestUnseen + 'episodes?' + of + title + ofin + 'season ' + season, re.I)))  # play (a) episode of <series> with <actor>
regex.append((70, 'TV Shows', re.compile(cmd + newestUnseen + 'episodes?' + ofin + 'season ' + season + of + title, re.I)))  # play (a) episode of <series> with <actor>
regex.append((60, 'TV Shows', re.compile(cmd + newestUnseen + 'episodes?' + of + title, re.I)))  # play (a) new(est) or unseen episode of <series>

regex.append((50, 'Movies', re.compile(cmd + newestUnseen + genreMovie + 'with' + any + actor, re.I)))    # play (newest, unseen) movie with <actor>
regex.append((40, 'Movies', re.compile(cmd + newestUnseen + genreMovie + of + '(the )?(director )?' + director, re.I)))  # play (newest, unseen) movie from director <director>
regex.append((30, 'Movies', re.compile(cmd + newestUnseen + genreMovie + of + time, re.I)))  # play a(ny) movie from the year or decade <year|decade>
regex.append((20, 'Movies', re.compile(cmd + newestUnseen + genreMovie + 'with( a)?( better| higher)? rating( above| better| higher| over)? (as|than|then) ' + higher_than_rating, re.I)))  # play a(ny) movie with a rating above <rating>
regex.append((20, 'Movies', re.compile(cmd + newestUnseen + genreMovie + 'with( a)?( worse| lower)? rating( below| worse| lower| under)? (as|than|then) ' + lower_than_rating, re.I)))  # play a(ny) movie with a rating above <rating>
regex.append((20, 'Movies', re.compile(cmd + newestUnseen + genreMovie + '(with( a)? content rating( of)?| (which|who) are rated) ' + contentRating, re.I)))  # play a(ny) movie with a content rating  R
regex.append((20, 'Movies', re.compile(cmd + newestUnseen + genreMovie + 'rated ' + contentRating, re.I)))  # play a(ny) R rated movie
regex.append((20, 'Movies', re.compile(cmd + newestUnseen + genreMovie + '$', re.I)))  # play a(ny) comedy (movie)
regex.append((20, 'Movies', re.compile(cmd + contentRating + ' rated ' + newestUnseen + genreMovie, re.I)))  # play a(ny) R rated movie
regex.append((10, None, re.compile(cmd + title, re.I)))   # play <title>


# combinations + refinement
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
