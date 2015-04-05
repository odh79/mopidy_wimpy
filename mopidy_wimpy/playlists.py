from __future__ import unicode_literals

import logging

from mopidy import backend
from mopidy.models import Playlist

logger = logging.getLogger(__name__)

class WimpyPlaylistsProvider(backend.PlaylistsProvider):
	
	#def __init__(self, *args, **kwargs):
	#	super(WimpyPlaylistsProvider, self).__init__(*args, **kwargs)
	
	
	def create(self, name):
		pass  # TODO
		
	def delete(self, uri):
		pass  # TODO
		
	def lookup(self, uri):
		logger.debug(u'Playlist lookup def. uri=%s' % uri)
		for playlist in self._playlists:
			if playlist.uri == uri:
				return playlist

	def refresh(self):
		playl = []
		playl.append(self.backend.session.get_playlist('ccba4c72-6aaf-43db-a46f-7f0cc579362d'))
		playl.append(self.backend.session.get_playlist('0c84fe6a-4cf1-425a-9598-f09eb377738b'))
		playl.append(self.backend.session.get_playlist('5d5b6916-3201-4293-ac8d-e204852c90f8'))
		playl.append(self.backend.session.get_playlist('14cb2e61-bd41-4aab-a03a-33b2d9a65181'))
		playl.append(self.backend.session.get_playlist('895a801a-eb62-4466-b811-6043c148fb98'))
		playlists = []
		
		tracks = []
		logger.info(u'Trying to load wimp playlists')
		# load user playlists
		#logger.debug(u'Playlists fetched: ')
		
			
		for playlist in self.backend.session.get_all_playlists():
		#for playlist in playl:
			tracks = []
			logger.debug(u'PlaylistId=%s' % playlist.id)
			for track in self.backend.session.get_playlist_tracks(playlist.id):
				if self.backend.library.lookup('wimpy:track:' + str(track.id)):
					
					track = self.backend.library.lookup('wimpy:track:' + str(track.id))
					logger.debug(u'result: %s' % track)
				else:
					self.backend.library._to_mopidy_track(track)
					tracks += self.backend.library.lookup('wimpy:track:' + str(track.id))
				
			logger.debug(u'tracks=%s' % tracks)
			playlist = Playlist(uri='wimpy:playlist:' + playlist.id, name=playlist.name, tracks=tracks)
			#playlist = Playlist(uri='wimp:playlist:' + playlist.id)
			
			playlists.append(playlist)
			self.playlists = playlists
			backend.BackendListener.send('playlists_loaded')
		logger.info(u'Loaded %s playlist from wimp' % len(playlists))
		self.playlists = playlists
		backend.BackendListener.send('playlists_loaded')
	def save(self, playlist):
		pass  # TODO