## NLPlexRemote ##
Natural language remote control for Plex clients.

[![Build Status](https://travis-ci.org/danielBreitlauch/NLPlexRemote.svg?branch=master)](https://travis-ci.org/danielBreitlauch/NLPlexRemote)

About
--------

NLPlexRemote allows you to control connected Plex clients with natural language commands.
One great usage is to combine it with either pocket sphinx, google speech or any other speech-to-text api.
The spoken command gets transformed into text and NLPlexRemote uses that to control your Plex client. 

Features
--------

* Play/pause or navigate to media on connected clients with relatively fuzzy natural language
* Find movies and tv shows by title, actors, release date, rating or everything combined
* Control subtitles and language
* Define and extend your language commands and meaning in a simple way
* English and German commands are already supported
* Use complex query combinations and context sensitive follow up commands


Installation
--------

NLPlexRemote is compatible with Python 2.7.  
There will be a pip package in the future.  
Until then... 
```
python ./setup.py install
```

Usage Examples
--------------

####First step: create the Remote:
You need the Url to your Plex server, the client name and a language definition.

```python
from NLPlexRemote import Remote, English
r = Remote(English(), 'http://192.168.0.30:32400', 'Swordmaster')
```

####Play a movie:
If there are multiple choices. It will pick one at random.

```python
r.execute('play an action movie with bruce willis')
r.execute('play any movie from the 60s')
r.execute('play an unseen romance')
```

####Follow up queries:
These are context aware commands that consider the commands from before.

```python
r.execute('go to any unseen episode from 88')
r.execute('filter episodes with patrick')
r.execute('another one')
r.execute('play it')
```

1. Pick one episode that was released 1988.
2. Retain all episodes with an actor named Patrick. Which brings you basically to Star Trek TNG.
3. It considers the requested media from before and chooses another episode from it.
4. Up until now the client just shows the detail pages of the found episodes. This command will play the episode.

Equivalent - Directly playing the episode:

```python
r.execute('play any episode of star trek the next generation season 2')
r.execute('play any episode with patrick from 1988')
```

####Language, Subtitles and other Controls:

```python
r.execute('turn subtitles on')
r.execute('switch subtitles')
r.execute('toggle language')
r.execute('pause movie')
```
