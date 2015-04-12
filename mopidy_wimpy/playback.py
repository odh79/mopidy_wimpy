from __future__ import unicode_literals

import logging

import time

from mopidy import backend

logger = logging.getLogger(__name__)


class WimpyPlaybackProvider(backend.PlaybackProvider):
	def __init__(self, audio, backend):
		super(WimpyPlaybackProvider, self).__init__(audio, backend)
		self._track_start = 0
		self._track = None

	def play(self, track):
		logger.debug('play(): %r', track)
		
		try:
			url = self.backend.session.get_media_url(track.uri.split(':')[2])
			#self.backend.session.play(1)
		except Exception as e:
			logger.debug('Exeption %s' % e)
			return
		self.audio.prepare_change()
		self.audio.set_uri(url).get()
		self._track_start = time.time()
		self._track = track
		return self.audio.start_playback().get()
	
	def resume(self):
		#self.backend.session.play(1)
		return super(WimpyPlaybackProvider, self).resume()
	
	def stop(self):
		logger.info(u'Player stoped')
		#self.backend.session.play(0)
		return super(WimpyPlaybackProvider,self).stop()
		