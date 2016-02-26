

def flat_map(video_tag):
    if len(video_tag) == 0:
        return None
    flat = video_tag[0].id
    for t in video_tag[1:]:
        flat += ',' + t.id
    video_tag[0].id = flat
    return video_tag[0]


def name_fit(name, actor):
    actor = actor.lower()
    if name == actor:
        return True
    for part in actor.split():
        if name == part:
            return True


def decade_fit(name, decade):
    name = name.lower().replace("s", "")
    decade = decade.lower().replace("s", "")
    if len(name) > 3:
        name = name[2:]
    if len(decade) > 3:
        decade = decade[2:]
    return name == decade


def case_insensitive_fit(rating, server_rating):
    return rating.lower() == server_rating.lower()


def filter_person(person_list, name):
    res = []
    for single_name in name.split('or'):
        res += [a for a in person_list if name_fit(single_name.strip(), a.tag)]
    return flat_map(res)


def filter_year(decades_list, name):
    return flat_map([a for a in decades_list if decade_fit(name, a.tag)])


def filter_case_insensitive(object_list, rating):
    return flat_map([a for a in object_list if case_insensitive_fit(rating, a.tag)])


def season_format(season):
    if 'season ' not in season:
        season = 'season ' + season
    return season


def filter_dict(dictionary, filter_keys):
    return dict([(item, dictionary[item]) for item in dictionary.keys() if item in filter_keys])
