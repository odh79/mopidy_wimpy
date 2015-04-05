from __future__ import unicode_literals

import logging
import re

from mopidy.models import Artist, Album, Playlist, Ref, Track

logger = logging.getLogger(__name__)

artist_cache = {}
album_cache = {}
track_cache = {}


def get_track_url(self, id):
	url = self.backend.session.get_media_url(id)
	return url
	
def to_mopidy_playlists(wimpy_playlists):
	playlists = []
	for playlist in wimpy_playlists:
		playlists.append(Ref.playlist(uri=playlist.id, name=playlist.name))
	return playlists

def to_mopidy_track_ref(self, track):
	uri = 'wimpy:track:' + str(track.id)
	return Ref.track(uri=uri, name=track.name)
	
	
def to_mopidy_track(self, track):
	#uri = get_track_url(self, track.id)
	uri = 'wimpy:track:' + str(track.id)
	
	track = Track(
		uri=uri,
		name=track.name,
		artists=[track.artist.name],
		album=track.album.name,
		track_no=int(track.track_num),
		disc_no=int(0),
		date=unicode(2015),
		length=int(track.duration*1000),
		bitrate=320)
	self.tracks[uri] = track
	
	return track