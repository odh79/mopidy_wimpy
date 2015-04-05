from __future__ import unicode_literals


import logging
import pykka
import time

from threading import Lock

from mopidy import backend

from mopidy_wimpy.library import WimpyLibraryProvider
from mopidy_wimpy.playback import WimpyPlaybackProvider
from mopidy_wimpy.repeating_timer import RepeatingTimer
from mopidy_wimpy.session import WimpySession
from mopidy_wimpy.playlists import WimpyPlaylistsProvider
									

#import wimpy

logger = logging.getLogger(__name__)

class WimpyBackend(pykka.ThreadingActor, backend.Backend):
	def __init__(self, config, audio):
		super(WimpyBackend, self).__init__()
		
		self.config = config
		self.trackdata = {}
		self._refresh_library_rate = 1440 * 60.0

			
		self._refresh_playlists_rate = 180 * 60.0

			
		self._refresh_library_timer = None
		self._refresh_playlists_timer = None
		self._refresh_lock = Lock()
		self._refresh_last = 0
        # do not run playlist refresh around library refresh
		self._refresh_threshold = self._refresh_playlists_rate * 0.3
		
		
		self.library = WimpyLibraryProvider(backend=self)
		self.playback = WimpyPlaybackProvider(audio=audio, backend=self)
		self.playlists = WimpyPlaylistsProvider(backend=self)
		self.session = WimpySession() 
		
		self.uri_schemes = ['wimpy']
		

		
	# Your backend implementation
	
	
	
	def on_start(self):
		logger.info('Mopidy uses WIMPY CORE')
		logger.debug('Connecting to Wimp')
		self.session.login(self.config['wimpy']['username'], self.config['wimpy']['password'])
		
		self._refresh_library_timer = RepeatingTimer(
			self._refresh_library,
			self._refresh_library_rate)
		self._refresh_library_timer.start()
        #schedule playlist refresh as desired
		if self._refresh_playlists_rate > 0:
			self._refresh_playlists_timer = RepeatingTimer(
				self._refresh_playlists,
				self._refresh_playlists_rate)
			self._refresh_playlists_timer.start()
		
	def on_stop(self):
		pass
	
	
	def _refresh_library(self):
		with self._refresh_lock:
			t0 = round(time.time())
			logger.info('Start refreshing Wimp Music library')
			self.playlists.refresh()
			self.library.refresh()
			t = round(time.time()) - t0
			logger.info('Finished refreshing Wimp Music content in %ds', t)
			self._refresh_last = t0
	
	def _refresh_playlists(self):
		if not self._refresh_lock.acquire(False):
            # skip, if library is already loading
			logger.debug(u'Wimpy: Skip refresh playlist : library refresh is running.')
			return
		t0 = round(time.time())
		if 0 < self._refresh_library_rate \
			< self._refresh_threshold + t0 - self._refresh_last:
            # skip, upcoming library refresh
			logger.debug(u'wimpy: Skip refresh playlist: ' +
                         'library refresh is around the corner')
			self._refresh_lock.release()
			return
		if self._refresh_last > t0 - self._refresh_threshold:
            # skip, library was just updated
			logger.debug(u'Wimpy: Skip refresh wimpy playlist: ' +
						'library just finished')
			self._refresh_lock.release()
			return
		logger.info(u'Start refreshing Wimp Music playlists')
		self.playlists.refresh()
		t = round(time.time()) - t0
		logger.info(u'Finished refreshing Wimp Music content in %ds', t)
		self._refresh_lock.release()