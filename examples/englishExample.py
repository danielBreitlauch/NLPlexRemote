
from NLPlexRemote import Remote, English

r = Remote(English(), 'http://192.168.0.30:32400', 'Swordmaster')

r.execute('go home')
# r.execute('go to any episode of how i met your mother from 2008')

#q.execute('go to any movie with alan from the 2010s')

exit(0)

r.execute('play episode of how i met your mother')
r.execute('go to any movie from the 60s')
r.execute('go to any unseen movie from 2010')
r.execute('go to any unseen movie rated PG-13')
r.execute('go to any new movie with bruce willis')
r.execute('go to any unseen movie with a rating higher than 8')
r.execute('go to a fistful of datas')
r.execute('go to any episode of how i met your mother from season 4')
r.execute('go to the newest episode of how mother in season 3')
r.execute('go to any unseen episode from limitless')
r.execute('go to a new episode from agent carter')
r.execute('go to an unseen romance')
r.execute('go to an unseen action movie')
r.execute('go to any new romance with george')
r.execute('go to any unseen action movie rated PG-13')
r.execute('go to any unseen action movie with a rating higher than 4')
r.execute('play newest episode with amy acker')

r.execute('go to any episode from 88')
r.execute('filter any episode with patrick')
r.execute('another one')
r.execute('play it')

r.execute('go to where were we?')

r.execute('pause movie')
r.execute('change language')
