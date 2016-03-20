

from formatHelper import FormatHelper, filter_dict
from plexapi.server import PlexServer
from random import Random
from datetime import datetime
import threading


class Remote:

    def __init__(self, language, plex_url, client_name):
        self.lang = language
        self.formatHelper = FormatHelper(language)
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
        self.filter_config = {'actor': self.formatHelper.filter_person,
                              'director': self.formatHelper.filter_person,
                              'writer': self.formatHelper.filter_person,
                              'producer': self.formatHelper.filter_person,
                              'year': self.formatHelper.filter_year,
                              'decade': self.formatHelper.filter_year,
                              'genre': self.formatHelper.filter_case_insensitive,
                              'country': self.formatHelper.filter_case_insensitive,
                              'contentRating': self.formatHelper.filter_case_insensitive}

        for section in self.plex.library.sections():
            if section.TYPE == 'movie':
                self.movies = section
            elif section.TYPE == 'show':
                self.shows = section

    def execute(self, text):
        print(text)
        commands = self.lang.match(text.lower())
        self.search(commands)
        self.filter_highest_priority()
        return self.execute_actions()

    def search(self, commands):
        self.found_media = []
        self.found_actions = []
        threads = []
        for priority, matched in commands:
            search_actions = [action for action in ['play', 'navigate', 'follow_up'] if action in matched]
            direct_actions = [action for action in ['another_one', 'play_it', 'main_menu', 'subtitle_on',
                                                    'subtitle_off', 'subtitle_toggle', 'language_toggle',
                                                    'osd', 'jump_forward', 'jump_backward',
                                                    'pause', 'play_after_pause'] if action in matched]

            if direct_actions:
                self.found_media.append((priority, direct_actions, None))
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

        multi_filters = self.create_filter(self.movies, matched)
        if multi_filters:
            results = self.movies.search(title, filter=movie_filter, **multi_filters.pop())
            for filters in multi_filters:
                filter_results = self.movies.search(title, filter=movie_filter, **filters)
                results = [result for result in results if result in filter_results]
            for video in self.post_filter(matched, results):
                self.found_media.append((priority, actions, video))

    def search_episodes(self, matched, priority, actions):
        title = matched.get('title')
        season = matched.get('season')

        if 'unseen' in matched:
            watched_filter = 'unwatched'
            matched['oldest'] = None
        else:
            watched_filter = 'all'

        show_multi_filters = self.create_filter(self.shows, filter_dict(matched, self.filterable_in_show))
        episode_multi_filters = self.create_filter(self.shows, filter_dict(matched, self.filterable_in_episode))
        if show_multi_filters is None or episode_multi_filters is None:
            return

        episode_set = []
        used_episode_filter = False
        if episode_multi_filters[0]:
            used_episode_filter = True
            episode_set = self.shows.searchEpisodes(None, filter=watched_filter, **episode_multi_filters.pop())
            for filters in episode_multi_filters:
                filter_episode_set = self.shows.searchEpisodes(title, filter=watched_filter, **filters)
                episode_set = [result for result in episode_set if result in filter_episode_set]

        results = []
        used_show_filter = False
        if show_multi_filters[0] or season or not used_episode_filter or title or watched_filter == 'unwatched':
            used_show_filter = True
            show_set = self.shows.search(title, filter=watched_filter, **show_multi_filters.pop())
            for filters in show_multi_filters:
                filter_show_set = self.shows.search(title, filter=watched_filter, **filters)
                show_set = [result for result in show_set if result in filter_show_set]
            for show in show_set:
                if season:
                    show = show.season(self.formatHelper.season_format(season))
                res = show.episodes(watched='unseen' not in matched)
                results += self.post_filter(matched, res)

        if used_episode_filter:
            if used_show_filter:
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
        multi_filter = [{}]
        for key, filter_method in self.filter_config.iteritems():
            entities = matched.get(key)
            if entities:
                server_entities = getattr(library, 'get_' + key)()
                for index, entity in enumerate(entities.split(self.lang.and_phrase())):
                    res = filter_method(server_entities, entity)
                    if res:
                        if len(multi_filter) <= index:
                            multi_filter.append(multi_filter[0].copy())
                        filters = multi_filter[index]
                        filters[key] = res
                    else:
                        return None

        return multi_filter

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
                highest_priority_actions += actions
                filtered.append(media)
        self.found_actions = highest_priority_actions
        self.found_media = filtered

    def execute_actions(self):
        if self.found_actions:
            print(self.found_actions[0])

        # direct actions
        if 'main_menu' in self.found_actions:
            self.client.stop()
        if 'subtitle_on' in self.found_actions:
            self.client.subtitle('on')
        if 'subtitle_off' in self.found_actions:
            self.client.subtitle('off')
        if 'subtitle_toggle' in self.found_actions:
            self.client.subtitle('next')
        if 'language_toggle' in self.found_actions:
            self.client.switch_language()
        if 'osd' in self.found_actions:
            self.client.toggleOSD()
        if 'jump_forward' in self.found_actions:
            self.client.stepForward()
        if 'jump_backward' in self.found_actions:
            self.client.stepBack()
        if 'pause' in self.found_actions:
            self.client.pause()
        if 'play_after_pause' in self.found_actions:
            self.client.play()
        if 'another_one' in self.found_actions:
            self.last_picked = self.pick_another_one()
            if self.last_picked:
                self.client.navigate(self.last_picked)
        if 'play_it' in self.found_actions:
            if self.last_picked:
                self.client.playMedia(self.last_picked)

        # search actions
        if 'follow_up' in self.found_actions or 'play' in self.found_actions or 'navigate' in self.found_actions:
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
        return len(self.found_actions) > 0

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
