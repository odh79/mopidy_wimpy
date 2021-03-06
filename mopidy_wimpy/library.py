﻿from __future__ import unicode_literals

import hashlib
import logging

from mopidy import backend
from mopidy.models import Album, Artist, Ref, SearchResult, Track

from mopidy_wimpy.translator import to_mopidy_track_ref, to_mopidy_playlists, local_to_mopidy_track_ref

logger = logging.getLogger(__name__)

class WimpyLibraryProvider(backend.LibraryProvider):
	root_directory = Ref.directory(uri='wimpy:directory', name='Wimp Music')
	
	def __init__(self, * args, **kwargs):
		#IMG_URL = "http://images.osl.wimpmusic.com/im/im?w={width}&h={height}&{id_type}={id}"
		self.IMG_URL = "http://varnish01.music.aspiro.com/im/im?w={width}&h={height}&{id_type}={id}"
		self.tracks = {}
		self.albums = {}
		self.artists = {}
		self.aa_artists = {}
		super(WimpyLibraryProvider, self).__init__(*args, **kwargs)
		 # TODO: add /artists/{top/tracks,albums/tracks} and /users?
		#self._root = [Ref.directory(uri='wimp:tracks:toplist',
		#							name='Personal top tracks'),
		#			Ref.directory(uri='wimp:albums:toplist',
		#							name='Personal top albums')]
		#self._root = [Ref.directory(uri='wimpy:directory:featured',
		self._root = [Ref.directory(uri='wimpy:featured:directorys',		
									name='Featured'),
					Ref.directory(uri='wimpy:moods',
									name='Moods'),
					Ref.directory(uri='wimpy:all',
									name='All tracks in local list')]
		
	def _browse_featured_directorys(self):
		logger.debug(u'Featured playlists')
		ddirectorys = []
		directorys = self.backend.session.get_featured()
		for d in directorys:
			#ttracks.append(to_mopidy_track_ref(self, t))
			ddirectorys.append(Ref.directory(uri=u'wimpy:featured:tracks:' + d.id,  name=d.name))
			logger.debug(u'Got featured %s:%s:%s' % (d.id, d.description, d.name))
			
		return ddirectorys
	
	def _browse_featured_tracks(self, uri):
		logger.info(u'Fetching featured tracks from wimp: ' + uri)
		id = uri.split(':')[3]
		ttracks = []
		tracks = self.backend.session.get_playlist_tracks(id)
		for t in tracks:
			ttracks.append(to_mopidy_track_ref(self, t))
			self._to_mopidy_track(t)
			#ttrack.append(self._to_mopidy_track(t))
			#directorys.append(Ref.directory(uri='wimpy:featured:directorys:' + t.name, name=t.name))
			logger.debug(u'Got track %s' % t.name)
			
		return ttracks
		
	def _browse_moods(self):
		logger.debug(u'Getting moods')
		mmoods = []
		moods = self.backend.session.get_moods()
		for m in moods:
			logger.debug(u'mood: %s' % m.name)
			mmoods.append(Ref.directory(uri=u'wimpy:mood:playlists:' + m.id, name=m.name))
			
		
		return mmoods 
		
	def _browse_mood_playlists(self, uri):
		mood = uri.split(':')[3]
		logger.debug(u'Getting mood %s tracks' % mood)
		playlists = []
		for p in self.backend.session.get_mood_playlists(mood):
			playlists.append(Ref.directory(uri=u'wimpy:mood:playlist:tracks:' + p.id,  name=p.name))
			logger.debug(u'Got featured %s:%s' % (p.id, p.name))
		return playlists
		
	def _browse_mood_playlist_tracks(self, uri):
		logger.info(u'Fetching mood playlist tracks from wimp: ' + uri)
		id = uri.split(':')[4]
		ttracks = []
		tracks = self.backend.session.get_playlist_tracks(id)
		for t in tracks:
			ttracks.append(to_mopidy_track_ref(self, t))
			self._to_mopidy_track(t)
			logger.debug(u'Got track %s' % t.name)
			
		return ttracks

	def _browse_genres(self):
		logger.debug(u'Getting genres')
		genres = []
		for g in self.backend.session.get_genres():
			logger.debug(u'genre: %s' % g.name)
			genres.append(Ref.directory(uri=u'wimpy:genre:tracks:' + g.id, name=g.name))
			
		
		return genres
		
	def _browse_genre_tracks(self, uri):
		logger.info(u'Fetching genre tracks from wimp: ' + uri)
		id = uri.split(':')[3]
		ttracks = []
		tracks = self.backend.session.get_playlist_tracks(id)
		for t in tracks:
			ttracks.append(to_mopidy_track_ref(self, t))
			self._to_mopidy_track(t)
			#ttrack.append(self._to_mopidy_track(t))
			#directorys.append(Ref.directory(uri='wimpy:featured:directorys:' + t.name, name=t.name))
			logger.debug(u'Got track %s' % t.name)
			
		return ttracks
		
	def _browse_all(self):
		tracks = []
		#logger.debug(u'self.tracks[] length %s' % len(self.tracks))
		for t in self.tracks:
			tracks.append(local_to_mopidy_track_ref(self, t))
			logger.debug(u'Track: %s:%s' % (t, self.tracks[t].name))
		
		return tracks
			
		
	def _browse_top_albums(self):
		return 
		
	#def _refresh(self, track):
	#	self._to_mopidy_track(track)
	
	def _to_mopidy_track(self, track):
	#uri = get_track_url(self, track.id)
		logger.debug('track = %s' % track.name)
		uri = 'wimpy:track:' + str(track.id)
		artist = self._to_mopidy_artist(track)
		try:
			track = self.tracks[uri]
			logger.debug(u'Track exists, returning from _to_mopidy_track')
		except:
			track = Track(
				uri=uri,
				name=track.name,
				artists=[artist],
				album=self._to_mopidy_album(track),
				track_no=int(track.track_num),
				disc_no=int(0),
				date=unicode(2015),
				length=int(track.duration*1000),
				bitrate=320)
			self.tracks[uri] = track
		logger.debug(u'%s tracks loaded' % len(self.tracks))
		return track
		
	def _to_mopidy_album(self, track):
		logger.debug(u'_to_mopidy_album. %s' % track.album.name)
		uri = 'wimpy:album:' + str(track.album.id)
		logger.debug(u'Going to try local database for album')
		try:
			#logger.debug(u'Going to try local database for album. Inside now with uri %s' % uri)
			album = self.albums[uri]
			#logger.debug(u'Album already exists %s albums loaded' % len(self.albums))
			return album
			
		except Exception as e:
			logger.debug('Downloading album: %s' % track.album.name)
			aalbum = self.backend.session.get_album(track.album.id)
			try :
				name = track.album.name
				num_tracks = int(aalbum.num_tracks)
				artist = self._to_mopidy_album_artist(track)
				date = u'2015'
				image = self.IMG_URL.format(width=512, height=512, id=track.album.id, id_type='albumid')
				logger.debug(u'Image = %s' % image )
				album = Album(
					uri=uri,
					name = name,
					artists = [artist],
					num_tracks=int(num_tracks),
					num_discs=0,
					date='2015',
					images=[image])
				self.albums[uri] = album
				logger.debug(u'Album downloaded. %s albums loaded' % len(self.albums))
				return album
			except:
				logger.debug(u'No album')
				return 
		
		
	
	def _to_mopidy_artist(self, track):
		name = track.artist.name
		uri = 'wimpy:artist:' + str(track.artist.id)
		
		artist = Artist(
			uri=uri,
			name=name)
		self.artists[uri] = artist
		return artist

	
	def _to_mopidy_album_artist(self, track):
		name = track.artist.name
		uri = 'wimpy:artist:' + str(track.artist.id)
		artist = Artist(
			uri=uri,
			name=name)
		self.artists[uri] = artist
		return artist			

		
	def browse(self, uri): 	
		#logger.info(u'wimp browser')
		logger.debug(u'wimp browse: %s', uri)
		
		
		if uri == self.root_directory.uri:
			#logger.debug('wimp self_root')
			return self._root

		if uri == 'wimpy:featured:directorys':
			logger.debug(u'getting wimp:directory:featured. And uri=%s' % uri)
			return self._browse_featured_directorys()
		
		if uri.startswith('wimpy:featured:tracks:'):
			logger.debug(u'getting wimp:tracks:featured. And uri=%s' % uri)
			return self._browse_featured_tracks(uri)
		
		
		if uri == 'wimpy:albums:favorite':
			logger.debug(u'getting wimp:albums:favorites')
			return self._browse_top_albums()
		
		if uri == 'wimpy:moods':
			return self._browse_moods()
		
		if uri.startswith('wimpy:mood:playlists:'):
			return self._browse_mood_playlists(uri)
		
		if uri.startswith('wimpy:mood:playlist:tracks:'):
			return self._browse_mood_playlist_tracks(uri)
			
		if uri == 'wimpy:genres':
			logger.debug(u'getting wimp:genres:featured. And uri=%s' % uri)
			return self._browse_genres()
		
		if uri.startswith('wimpy:genre:tracks:'):
			logger.debug(u'getting wimp:genre:tracks. And uri=%s' % uri)
			return self._browse_genre_tracks(uri)
		
		if uri == 'wimpy:all':
			logger.debug(u'Getting genre tracks')
			return self._browse_all()
			
		else:
			logger.info(u'Did not find option to browse')
	
	def search(self, field, value):
		return self.api.search(field, value)
		
	def _lookup_track(self, uri):
		try:
			logger.debug(u'lookup track %s' % uri)
			track = self.tracks[uri]
			logger.debug(u'self.track %s' % self.tracks[uri])
		except Exception as e:
			logger.debug(u'Error: %s' % e)
			return []
		return [self.tracks[uri]]
	
	
	
	def _lookup_album(self, uri):
		album = self.backend.session.get_album_tracks(uri.split(':')[2])
		tracks = []
		logger.debug(u'lookup album %s' % uri)
		for t in album:
			track_uri = 'wimpy:track:' + str(t.id)
			logger.debug(u'Track is in local db')
			try:
				track = self.tracks[track_uri]
				logger.debug(u'Track exists')
			except Exception as e:
				logger.debug(u'Exception is %s' % e)
				logger.debug(u'Track is new, adding')
				self._to_mopidy_track(t)
			tracks.append(self.tracks[track_uri])
		return tracks

	
	def _lookup_artist(self, uri):
		logger.debug(u'lookup artist %s' % uri)
		tracks = []
		artist_id = uri.split(':')[2]
		tracks_in = self.backend.session.get_artist_top_tracks(artist_id)
		for t in tracks_in:
			track_uri = 'wimpy:track:' + str(t.id)
			logger.debug(u'Track is in local db')
			try:
				track = self.tracks[track_uri]
				logger.debug(u'Track exist')
			except Exception as e:
				logger.debug(u'Exception %s' % e)
				logger.debug(u'Track is new, adding')
				self._to_mopidy_track(t)
			tracks.append(self.tracks[track_uri])
		
		return tracks
	
	def _lookup_playlist(self, uri):
		playlist = self.backend.session.get_playlist_tracks(uri.split(':')[2])
		tracks = []
		logger.debug(u'lookup playlist %s' % uri)
		for t in playlist:
			track_uri = 'wimpy:track:' + str(t.id)
			logger.debug(u'Track is in local db')
			try:
				track = self.tracks[track_uri]
				logger.debug(u'Track exists')
			except Exception as e:
				logger.debug(u'Exception is %s' % e)
				logger.debug(u'Track is new, adding')
				self._to_mopidy_track(t)
			tracks.append(self.tracks[track_uri])
		return tracks
		
	
	def lookup(self, uri):
		logger.debug('wimpy lookup uri=%s' % uri)
		if uri.startswith('wimpy:track:'):
			return self._lookup_track(uri)
		elif uri.startswith('wimpy:album:'):
			return self._lookup_album(uri)
		elif uri.startswith('wimpy:artist:'):
			return self._lookup_artist(uri)
		elif uri.startswith('wimpy:playlist:'):
			return self._lookup_playlist(uri)
		else:
			return []
	

	
	def refresh(self):
		#self.tracks = {}
		#self.albums = {}
		#self.artists = {}
		#self.aa_artists = {}
		logger.debug(u'library.py Refresh')
		for track in self.backend.session.get_all_tracks():
			self._to_mopidy_track(track)
		logger.debug(u'All tracks recieved')
	
	def _create_id(self, u):
		return hashlib.md5(u.encode('utf-8')).hexdigest()
