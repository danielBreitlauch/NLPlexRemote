import threading

from englishRex import match
from plexapi.server import PlexServer

plex = PlexServer("http://192.168.0.30:32400")
client = plex.client("Swordmaster")

movies = plex.library.section('Movies')
shows = plex.library.section('TV Shows')


def flatmap_tag(videoTag):
    if len(videoTag) == 0:
        return None
    flat = videoTag[0].id
    for t in videoTag[1:]:
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


def case_insensitive_fitt(rating, serverRating):
    return rating.lower() == serverRating.lower()


def filter_person(person_list, name):
    return flatmap_tag([a for a in person_list if name_fitt(name, a.tag)])


def filter_year(decades_list, name):
    return flatmap_tag([a for a in decades_list if decade_fitt(name, a.tag)])


def filter_case_insensitive(object_list, rating):
    return flatmap_tag([a for a in object_list if case_insensitive_fitt(rating, a.tag)])


def season_format(season):
    if 'season ' not in season:
        season = 'season ' + season
    return season


def create_filter(matched):
    args = dict()
    if 'actor' in matched:
        res = filter_person(movies.get_actor(), matched['actor'])
        if res is None:
            return None
        args['actor'] = res

    if 'director' in matched:
        res = filter_person(movies.get_director(), matched['director'])
        if res is None:
            return None
        args['director'] = res

    if 'writer' in matched:
        res = filter_person(movies.get_writer(), matched['writer'])
        if res is None:
            return None
        args['writer'] = res

    if 'producer' in matched:
        res = filter_person(movies.get_producer(), matched['producer'])
        if res is None:
            return None
        args['producer'] = res

    if 'year' in matched:
        res = filter_year(movies.get_year(), matched['year'])
        if res is None:
            return None
        args['year'] = res

    if 'decade' in matched:
        res = filter_year(movies.get_decade(), matched['decade'])
        if res is None:
            return None
        args['decade'] = res

    if 'genre' in matched:
        res = filter_case_insensitive(movies.get_genre(), matched['genre'])
        if res is None:
            return None
        args['genre'] = res

    if 'country' in matched:
        res = filter_case_insensitive(movies.get_country(), matched['country'])
        if res is None:
            return None
        args['country'] = res

    if 'contentRating' in matched:
        res = filter_case_insensitive(movies.get_content_rating(), matched['contentRating'])
        if res is None:
            return None
        args['contentRating'] = res
    return args


def post_filter(matched, results):
    if 'higher_rating' in matched and results:
        border = float(matched['higher_rating'])
        results = [video for video in results if hasattr(video, 'rating') and float(video.rating) > border]

    if 'lower_rating' in matched and results:
        border = float(matched['lower_rating'])
        results = [video for video in results if hasattr(video, 'rating') and float(video.rating) < border]

    if 'newest' in matched and len(results) > 1:
        newest = results[0]
        newest_date = results[0].originallyAvailableAt
        for video in results:
            if video.originallyAvailableAt > newest_date:
                newest_date = video.originallyAvailableAt
                newest = video
        return [newest]

    if 'oldest' in matched and len(results) > 1:
        oldest = results[0]
        oldest_date = results[0].originallyAvailableAt
        for video in results:
            if video.originallyAvailableAt < oldest_date:
                oldest_date = video.originallyAvailableAt
                oldest = video
        return [oldest]
    return results


def search_movies(matched, found, priority):
    title = matched.get('title')

    if 'unseen' in matched:
        movie_filter = 'unwatched'
    else:
        movie_filter = 'all'

    args = create_filter(matched)
    if args is None:
        return

    results = movies.search(title, filter=movie_filter, **args)
    results = post_filter(matched, results)
    for video in results:
        found.append((priority, video))


def search_episodes(matched, found, priority):
    title = matched.get('title')
    season = matched.get('season')

    if 'unseen' in matched:
        episode_filter = 'unwatched'
        matched['oldest'] = 'added'
    else:
        episode_filter = 'all'

    results = []
    if title:
        found_shows = shows.search(title, filter=episode_filter)
        for show in found_shows:
            if season:
                season = show.season(season_format(season))
                results = season.episodes()
            else:
                results = show.episodes(watched='unseen' not in matched)
    else:
        results = shows.searchEpisodes(None, filter=episode_filter)

    results = post_filter(matched, results)
    for video in results:
        found.append((priority, video))


def search_general(matched, found, priority):
    title = matched.get('title')
    results = plex.search(title)
    results = post_filter(matched, results)
    for video in results:
        found.append((priority, video))


# solutions = match("go home")
# solutions = match("play episode of how i met your mother")
# solutions = match("go to any movie from the 60s")
# solutions = match("go to any unseen movie from 2010")
# solutions = match("go to any unseen movie rated PG-13")
# solutions = match("go to any new movie with bruce willis")
# solutions = match("go to any unseen movie with a rating higher than 8")
# solutions = match("go to a fistful of datas")
# solutions = match("go to any episode of how i met your mother from season 4")
# solutions = match("go to the newest episode of how mother in season 3")
# solutions = match("go to any unseen episode from limitless")
# solutions = match("go to a new episode from agent carter")
# solutions = match("go to an unseen romance")
# solutions = match("go to an unseen action movie")
# solutions = match("go to any new romance with george")
# solutions = match("go to any unseen action movie rated PG-13")
# solutions = match("go to any unseen action movie with a rating higher than 4")


found = []
threads = []
for matched, priority in solutions:
    print(matched)
    if 'category' not in matched:
        thr = threading.Thread(target=search_general, args=[matched, found, priority])
    elif matched['category'] == 'TV Shows':
        thr = threading.Thread(target=search_episodes, args=[matched, found, priority])
    elif matched['category'] == 'Movies':
        thr = threading.Thread(target=search_movies, args=[matched, found, priority])

    threads.append(thr)
    thr.start()
    thr.join()

# for thr in threads:
#    thr.join()
print(found)


# TODO: support author1 and author2

# def search(self, title, filter='all', vtype=None, **tags):
#        """ Search section content.
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
