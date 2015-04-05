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
		except Exception as e:
			logger.debug('Exeption %s' % e)
			return
		self.audio.prepare_change()
		self.audio.set_uri(url).get()
		self._track_start = time.time()
		self._track = track
		return self.audio.start_playback().get()

    def stop(self):
		logger.info(u'Player stoped')
        #super(WimpyPlaybackProvider, self).stop()
        #if not self._track:
        #    logger.debug('Current track is unset')
        #elif 0 < self._track.length * 2/3 \
        #       < (time.time() - self._track_start) * 1000:
        #    track_id = self._track.uri.split(':')[2]
        #    logger.debug('Broadcast play to google music: %r', track_id)
        #    self.backend.session.increment_song_playcount(track_id)
        #    self._track = None  # prevent additional calls
        #else:
        #    logger.debug('Track got skipped') 