from __future__ import unicode_literals

import logging

from wimpy import Session

class WimpySession():
	
	def __init__(self):
		super(WimpySession, self).__init__()
		logger.info('Mopidy uses Wimp')
		self.api = Session()
		
	def login(self, username, password):
		self.api.login(username, password)
		
	def logout(self):
		pass
		
	def get_stream_url(self, song_id):
		url = self.api.self.backend.session.get_media_url(song_id)
		if not url.startswith('http://') and not url.startswith('https://'):
			host, app, playpath = url.split('/', 3)
			url = 'rtmp://%s app=%s playpath=%s' % (host, app, playpath)
		return url
		
	def get_all_playlists(self):
            return self.api.get_all_playlists(self.api.user.id)
			
	
	def get_thumbs_up_songs(self):
		return self.api.get_favorite_tracks(self.api.user.id)

		