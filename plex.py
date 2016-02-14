import threading

from englishRex import match
from plexapi.server import PlexServer

plex = PlexServer("http://192.168.0.30:32400")
client = plex.client("Swordmaster")

movies = plex.library.section('Movies')
tv = plex.library.section('TV Shows')


def flatMapTag(videoTag):
    if len(videoTag) == 0:
        return None
    flat = ''
    for t in videoTag:
        flat += ',' + t.id
    videoTag[0].id = flat
    return videoTag[0]


def name_fitt(name, actor):
    actor = actor.lower()
    if name == actor:
        return True
    for part in actor.split():
        if name == part:
            return True


def decade_fitt(name, decade):
    name = name.lower().replace("s", "")
    decade = decade.lower().replace("s", "")
    if len(name) > 3:
        name = name[2:]
    if len(decade) > 3:
        decade = decade[2:]
    return name == decade


def filter_person(plist, name):
    return flatMapTag([a for a in plist if name_fitt(name, a.tag)])


def filter_decade(decadeslist, name):
    d = [d for d in decadeslist if decade_fitt(name, d)]
    if len(d) > 0:
        return d[0]
    return None


def search(matched, found, priority):
    title = matched.get('title')

    newest = matched.get('newest')
    unseen = matched.get('unseen')
    year = matched.get('year')
    rating = matched.get('rating')
    season = matched.get('season')
    contentRating = matched.get('contentRating')


    filter = 'all'


    args = dict()
    if 'actor' in matched:
        res = filter_person(movies.actorObj(), matched['actor'])
        if res is None:
            return
        args['actor'] = res

    if 'director' in matched:
        res = filter_person(movies.directorObj(), matched['director'])
        if res is None:
            return
        args['director'] = res

    dec = None
    if 'decade' in matched:
        res = filter_decade(movies.decade(), matched['decade'])
        if res is None:
            return
        dec = movies.decade(res)

    if 'category' in matched:
        section = plex.library.section(matched['category'])
        search = section.search(title, filter='all', **args)
        if dec:
            search = [video for video in search if video in dec]

        for video in search:
            found.append((priority, video))
    else:
        section = plex
        for video in section.search(title):
            found.append(video)


# solution = match("go home")
# solutions = match("play episode of how i met your mother")
solutions = match("go to any movie from the 60s")

found = []
threads = []
for s, priority in solutions:
    print(s)
    thr = threading.Thread(target=search, args=[s, found, priority])
    threads.append(thr)
    thr.start()
    thr.join()

# for thr in threads:
#    thr.join()
print(found)


# TODO: support author1 and author2

# def search(self, title, filter='all', vtype=None, **tags):
#        """ Search section content.
#            title: Title to search (pass None to search all titles).
#            filter: One of {'all', 'newest', 'onDeck', 'recentlyAdded', 'recentlyViewed', 'unwatched'}.
#            videotype: One of {'movie', 'show', 'season', 'episode'}.
#            tags: One of {country, director, genre, producer, actor, writer}.
#        """


# for section in plex.library.sections():
#    print('Unwatched content in %s:' % section.title)
#    for video in section.unwatched():
#        print('  %s' % video.title)


# Example 7: List files for the latest episode of Friends.
# the_last_one = plex.library.get('Friends').episodes()[-1]
# for part in the_last_one.iter_parts():
#    print(part.file)
