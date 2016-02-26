from random import Random
from plexapi.server import PlexServer
from datetime import datetime
import threading
from plex_helper import filter_dict, season_format, filter_case_insensitive, filter_year, filter_person


class Query:

    def __init__(self, language, plex_url, client_name):
        self.lang = language
        self.plex = PlexServer(plex_url)
        self.client = self.plex.client(client_name)

        # last results for context awareness
        self.found_media = []
        self.found_actions = []
        self.last_request = []
        self.last_picked = None

        # filter configuration
        self.filterable_in_episode = ['director', 'writer', 'year', 'decade']
        self.filterable_in_show = ['actor', 'genre', 'contentRating']
        self.filter_config = {'actor': filter_person,
                              'director': filter_person,
                              'writer': filter_person,
                              'producer': filter_person,
                              'year': filter_year,
                              'decade': filter_year,
                              'genre': filter_case_insensitive,
                              'country': filter_case_insensitive,
                              'contentRating': filter_case_insensitive}

        for section in self.plex.library.sections():
            if section.TYPE == 'movie':
                self.movies = section
            elif section.TYPE == 'show':
                self.shows = section

    def execute(self, text):
        print(text)
        commands = self.lang.match(text)
        self.search(commands)
        self.filter_highest_priority()
        self.execute_actions()

    def search(self, commands):
        self.found_media = []
        self.found_actions = []
        threads = []
        for priority, matched in commands:
            search_actions = [action for action in ['play', 'navigate', 'follow_up'] if action in matched]
            direct_actions = [action for action in ['another_one', 'play_it', 'main_menu', 'subtitle_on', 'subtitle_off',
                                                    'subtitle_toggle', 'language_toggle', 'osd', 'jump_forward',
                                                    'jump_backward', 'pause_toggle'] if action in matched]

            if direct_actions:
                self.found_media.append((priority, direct_actions, []))
            else:
                if 'movie' in matched:
                    function = self.search_movies
                elif 'tv' in matched:
                    function = self.search_episodes
                else:
                    function = self.search_general
                thr = threading.Thread(target=function, args=[matched, priority, search_actions])
                threads.append(thr)
                thr.start()
        for thr in threads:
            thr.join()

    def search_movies(self, matched, priority, actions):
        title = matched.get('title')

        if 'unseen' in matched:
            movie_filter = 'unwatched'
        else:
            movie_filter = 'all'

        args = self.create_filter(self.movies, matched)
        if args is not None:
            results = self.movies.search(title, filter=movie_filter, **args)
            results = self.post_filter(matched, results)
            for video in results:
                self.found_media.append((priority, actions, video))

    def search_episodes(self, matched, priority, actions):
        title = matched.get('title')
        season = matched.get('season')

        if 'unseen' in matched:
            episode_filter = 'unwatched'
            matched['oldest'] = 'added'
        else:
            episode_filter = 'all'

        show_args = self.create_filter(self.shows, filter_dict(matched, self.filterable_in_show))
        episode_args = self.create_filter(self.shows, filter_dict(matched, self.filterable_in_episode))
        if show_args is None or episode_args is None:
            return

        episode_set = []
        if episode_args:
            episode_set = self.shows.searchEpisodes(title, filter=episode_filter, **episode_args)

        results = []
        if show_args or season or not episode_args:
            for show in self.shows.search(title, filter=episode_filter, **show_args):
                if season:
                    show = show.season(season_format(season))
                results += show.episodes(watched='unseen' not in matched)

        if episode_args:
            if show_args or season:
                results = [result for result in results if result in episode_set]
            else:
                results = episode_set

        results = self.post_filter(matched, results)
        for video in results:
            self.found_media.append((priority, actions, video))

    def search_general(self, matched, priority, actions):
        title = matched.get('title')
        results = self.plex.search(title)
        results = self.post_filter(matched, results)
        for video in results:
            self.found_media.append((priority, actions, video))

    def create_filter(self, library, matched):
        filters = dict()
        for key, (retrieve_method, filter_method) in self.filter_config.iteritems():
            entity = matched.get(key)
            if entity:
                retrieve_method = getattr(library, 'get_' + key)
                res = filter_method(retrieve_method(), entity)
                if res:
                    filters[key] = res
                else:
                    return None

        return filters

    @staticmethod
    def post_filter(matched, results):
        if 'higher_rating' in matched and results:
            border = float(matched['higher_rating'])
            results = [video for video in results if hasattr(video, 'rating') and float(video.rating) > border]

        if 'lower_rating' in matched and results:
            border = float(matched['lower_rating'])
            results = [video for video in results if hasattr(video, 'rating') and float(video.rating) < border]

        if 'newest' in matched and len(results) > 1:
            newest = results[0]
            newest_date = datetime(1, 1, 1)
            for video in results:
                if hasattr(video, 'originallyAvailableAt') and video.originallyAvailableAt > newest_date:
                    newest_date = video.originallyAvailableAt
                    newest = video
            return [newest]

        if 'oldest' in matched and len(results) > 1:
            oldest = results[0]
            oldest_date = datetime(9999, 1, 1)
            for video in results:
                if hasattr(video, 'originallyAvailableAt') and video.originallyAvailableAt < oldest_date:
                    oldest_date = video.originallyAvailableAt
                    oldest = video
            return [oldest]
        return results

    def filter_highest_priority(self):
        highest_priority = -1
        for priority, actions, media in self.found_media:
            highest_priority = max(priority, highest_priority)

        filtered = []
        highest_priority_actions = []
        for priority, actions, media in self.found_media:
            if priority == highest_priority:
                highest_priority_actions.append(actions)
                filtered.append(media)
        self.found_actions = highest_priority_actions
        self.found_media = filtered

    def execute_actions(self):
        for action in self.found_actions:
            print(action)

        if not self.found_media:
            # direct actions
            if 'main_menu' in self.found_actions:
                self.client.stop()
            if 'subtitle_on' in self.found_actions:
                self.client.subtitle("on")
            if 'subtitle_off' in self.found_actions:
                self.client.subtitle("off")
            if 'subtitle_toggle' in self.found_actions:
                self.client.subtitle("next")
            if 'language_toggle' in self.found_actions:
                self.client.switch_language()
            if 'osd' in self.found_actions:
                self.client.toggleOSD()
            if 'jump_forward' in self.found_actions:
                self.client.stepForward()
            if 'jump_backward' in self.found_actions:
                self.client.stepBack()
            if 'pause_toggle' in self.found_actions:
                self.client.pause()
            if 'another_one' in self.found_actions:
                self.last_picked = self.pick_another_one()
                self.client.navigate(self.last_picked)
            if 'play_it' in self.found_actions:
                self.client.playMedia(self.last_picked)
        else:
            # search actions
            if 'follow_up' in self.found_actions:
                self.found_media = [f for f in self.found_media if f in self.last_request]

            self.last_picked = self.pick_one()
            self.last_request = self.found_media
            if self.last_picked:
                if 'play' in self.found_actions:
                    print('play ' + str(self.last_picked))
                    self.client.playMedia(self.last_picked)
                elif 'navigate' in self.found_actions:
                    print('go to ' + str(self.last_picked))
                    self.client.navigate(self.last_picked)

    def pick_one(self):
        if len(self.found_media) == 0:
            return None
        pos = Random().randint(0, len(self.found_media) - 1)
        return self.found_media[pos]

    def pick_another_one(self):
        if len(self.last_request) == 0:
            return None
        if len(self.last_request) == 1:
            return self.last_request[0]

        video = None
        while not video or video == self.last_picked:
            video = self.last_request[Random().randint(0, len(self.last_request) - 1)]
        return video


# TODO: support author1 and author2
# if both are in query plex will <or> them together
