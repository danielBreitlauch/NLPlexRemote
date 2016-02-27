

class FormatHelper:

    def __init__(self, lang):
        self.lang = lang

    @staticmethod
    def name_fit(name, actor):
        actor = actor.lower()
        if name == actor:
            return True
        for part in actor.split():
            if name == part:
                return True

    def decade_fit(self, name, decade):
        name = name.lower().replace(self.lang.decade_plural_phrase(), "")
        decade = decade.lower().replace(self.lang.decade_plural_phrase(), "")
        if len(name) > 3:
            name = name[2:]
        if len(decade) > 3:
            decade = decade[2:]
        return name == decade

    @staticmethod
    def case_insensitive_fit(rating, server_rating):
        return rating.lower() == server_rating.lower()

    def filter_person(self, person_list, name):
        res = []
        # put both ids in a list for plex, if both are in query plex will load every media with at least one of them
        for single_name in name.split(self.lang.or_phrase()):
            res += [a for a in person_list if self.name_fit(single_name.strip(), a.tag)]
        return flat_map(res)

    def filter_year(self, decades_list, name):
        res = []
        for single_decade in name.split(self.lang.or_phrase()):
            res += [a for a in decades_list if self.decade_fit(single_decade, a.tag)]
        return flat_map(res)

    def filter_case_insensitive(self, object_list, objects):
        res = []
        for single_object in objects.split(self.lang.or_phrase()):
            res += [a for a in object_list if self.case_insensitive_fit(single_object, a.tag)]
        return flat_map(res)

    @staticmethod
    def season_format(season):
        if 'season ' not in season:
            season = 'season ' + season
        return season


def flat_map(video_tag):
    if len(video_tag) == 0:
        return None
    flat = video_tag[0].id
    for t in video_tag[1:]:
        flat += ',' + t.id
    video_tag[0].id = flat
    return video_tag[0]


def filter_dict(dictionary, filter_keys):
    return dict([(item, dictionary[item]) for item in dictionary.keys() if item in filter_keys])
