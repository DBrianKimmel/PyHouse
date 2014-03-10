#!/usr/bin/env python

""" DIDL = Digital Item Description Language

Licensed under the MIT license
http://opensource.org/licenses/mit-license.php

Copyright 2005, Tim Potter <tpot@samba.org>
Copyright 2006-2008 John-Mark Gurney <jmg@funkthat.com>

"""

__version__ = '1.0.0'

from xml.etree.ElementTree import Element, SubElement, tostring, _ElementInterface

class Resource(object):
	"""An object representing a resource."""

	validattrs = {
		'protocolinfo':		'protocolInfo',
		'importuri':		'importUri',
		'size':			'size',
		'duration':		'duration',
		'protection':		'protection',
		'bitrate':		'bitrate',
		'bitspersample':	'bitsPerSample',
		'samplefrequency':	'sampleFrequence',
		'nraudiochannels':	'nrAudioChannels',
		'resolution':		'resolution',
		'colordepth':		'colorDepth',
		'tspec':		'tspec',
		'alloweduse':		'allowedUse',
		'validitystart':	'validityStart',
		'validityend':		'validityEnd',
		'remainingtime':	'remainingTime',
		'usageinfo':		'usageInfo',
		'rightsinfouri':	'rightsInfoURI',
		'contentinfouri':	'contentInfoURI',
		'recordquality':	'recordQuality',
	}

	def __init__(self, data, protocolInfo):
		object.__init__(self)
		# Use these so setattr can be more simple
		object.__setattr__(self, 'data', data)
		object.__setattr__(self, 'attrs', {})
		self.protocolInfo = protocolInfo

	def __getattr__(self, key):
		try:
			return self.attrs[key.lower()]
		except KeyError:
			raise AttributeError, key

	def __setattr__(self, key, value):
		key = key.lower()
		assert key in self.validattrs
		self.attrs[key] = value

	def toElement(self):
		root = Element('res')
		root.text = self.data
		for i in self.attrs:
			root.attrib[self.validattrs[i]] = str(self.attrs[i])
		return root

class ResourceList(list):
	'''Special class to not overwrite mimetypes that already exist.'''
	def __init__(self, *args, **kwargs):
		self._mt = {}
		list.__init__(self, *args, **kwargs)

	def append(self, k):
		assert isinstance(k, Resource)
		mt = k.protocolInfo.split(':')[2]
		if self._mt.has_key(mt):
			return
		list.append(self, k)
		self._mt[mt] = k

class Object(object):
	"""The root class of the entire content directory class heirachy."""

	klass = 'object'
	creator = None
	res = None
	writeStatus = None
	content = property(lambda x: x._content)
	needupdate = None  # do we update before sending? (for res)

	def __init__(self, cd, p_id, parentID, title, restricted = False,
                        creator = None, **kwargs):
		self.cd = cd
		self.id = p_id
		self.parentID = parentID
		self.title = title
		self.creator = creator
		if restricted:
			self.restricted = '1'
		else:
			self.restricted = '0'
		if kwargs.has_key('content'):
			self._content = kwargs['content']

	def __lt__(self, other):
		return self.__cmp__(other) < 0

	def __le__(self, other):
		return self.__cmp__(other) <= 0

	def __eq__(self, other):
		return self.__cmp__(other) == 0

	def __ne__(self, other):
		return self.__cmp__(other) != 0

	def __gt__(self, other):
		return self.__cmp__(other) > 0

	def __ge__(self, other):
		return self.__cmp__(other) >= 0

	def __cmp__(self, other):
		if not isinstance(other, self.__class__):
			return 1
		return cmp(self.id, other.id)

	def __repr__(self):
		cls = self.__class__
		return '<%s.%s: id: %s, parent: %s, title: %s>' % \
		    (cls.__module__, cls.__name__, self.id, self.parentID,
		    self.title)

	def checkUpdate(self):
		return self

	def toElement(self):
		root = Element(self.elementName)
		root.attrib['id'] = self.id
		root.attrib['parentID'] = self.parentID
		SubElement(root, 'dc:title').text = self.title
		SubElement(root, 'upnp:class').text = self.klass
		root.attrib['restricted'] = self.restricted
		if self.creator is not None:
			SubElement(root, 'dc:creator').text = self.creator
		if self.res is not None:
			try:
				for res in iter(self.res):
					root.append(res.toElement())
			except TypeError:
				root.append(self.res.toElement())
		if self.writeStatus is not None:
			SubElement(root, 'upnp:writeStatus').text = self.writeStatus
		return root

	def toString(self):
		return tostring(self.toElement())

class Item(Object):
	"""A class used to represent atomic (non-container) content objects.
        """
	klass = Object.klass + '.item'
	elementName = 'item'
	refID = None
	needupdate = True

	def doUpdate(self):
		# Update parent container
		Container.doUpdate(self.cd[self.parentID])

	def toElement(self):
		root = Object.toElement(self)
		if self.refID is not None:
			SubElement(root, 'refID').text = self.refID
		return root

class ImageItem(Item):
	klass = Item.klass + '.imageItem'

class Photo(ImageItem):
	klass = ImageItem.klass + '.photo'

class AudioItem(Item):
	"""A piece of content that when rendered generates some audio."""

	klass = Item.klass + '.audioItem'
	genre = None
	description = None
	longDescription = None
	publisher = None
	language = None
	relation = None
	rights = None

	def toElement(self):
		root = Item.toElement(self)
		if self.genre is not None:
			SubElement(root, 'upnp:genre').text = self.genre
		if self.description is not None:
			SubElement(root, 'dc:description').text = self.description
		if self.longDescription is not None:
			SubElement(root, 'upnp:longDescription').text = \
			    self.longDescription
		if self.publisher is not None:
			SubElement(root, 'dc:publisher').text = self.publisher
		if self.language is not None:
			SubElement(root, 'dc:language').text = self.language
		if self.relation is not None:
			SubElement(root, 'dc:relation').text = self.relation
		if self.rights is not None:
			SubElement(root, 'dc:rights').text = self.rights
		return root

class MusicTrack(AudioItem):
	"""A discrete piece of audio that should be interpreted as music."""

	klass = AudioItem.klass + '.musicTrack'
	artist = None
	album = None
	originalTrackNumber = None
	playlist = None
	storageMedium = None
	contributor = None
	date = None

	def toElement(self):
		root = AudioItem.toElement(self)
		if self.artist is not None:
			SubElement(root, 'upnp:artist').text = self.artist
		if self.album is not None:
			SubElement(root, 'upnp:album').text = self.album
		if self.originalTrackNumber is not None:
			SubElement(root, 'upnp:originalTrackNumber').text = \
			    self.originalTrackNumber
		if self.playlist is not None:
			SubElement(root, 'upnp:playlist').text = self.playlist
		if self.storageMedium is not None:
			SubElement(root, 'upnp:storageMedium').text = self.storageMedium
		if self.contributor is not None:
			SubElement(root, 'dc:contributor').text = self.contributor
		if self.date is not None:
			SubElement(root, 'dc:date').text = self.date
		return root

class AudioBroadcast(AudioItem):
	klass = AudioItem.klass + '.audioBroadcast'

class AudioBook(AudioItem):
	klass = AudioItem.klass + '.audioBook'

class VideoItem(Item):
	klass = Item.klass + '.videoItem'

class Movie(VideoItem):
	klass = VideoItem.klass + '.movie'

class VideoBroadcast(VideoItem):
	klass = VideoItem.klass + '.videoBroadcast'

class MusicVideoClip(VideoItem):
	klass = VideoItem.klass + '.musicVideoClip'

class PlaylistItem(Item):
	klass = Item.klass + '.playlistItem'

class TextItem(Item):
	klass = Item.klass + '.textItem'


class Container(Object, list):
	"""An object that can contain other objects.
        """

	klass = Object.klass + '.container'
	elementName = 'container'
	childCount = property(lambda x: len(x))
	createClass = None
	searchClass = None
	searchable = None
	updateID = 0
	needupdate = False

	def __init__(self, cd, p_id, parentID, title, restricted = 0,
	    creator = None, **kwargs):
		Object.__init__(self, cd, p_id, parentID, title, restricted,
		    creator, **kwargs)
		list.__init__(self)

	def doUpdate(self):
		if self.id == '0':
			self.updateID = (self.updateID + 1)
		else:
			self.updateID = (self.updateID + 1) % (1l << 32)
			Container.doUpdate(self.cd['0'])

	def toElement(self):
		root = Object.toElement(self)
		# only include if we have children, it's possible we don't
		# have our children yet, and childCount is optional.
		if self.childCount:
			root.attrib['childCount'] = str(self.childCount)
		if self.createClass is not None:
			SubElement(root, 'upnp:createclass').text = self.createClass
		if self.searchClass is not None:
			if not isinstance(self.searchClass, (list, tuple)):
				self.searchClass = ['searchClass']
			for i in self.searchClass:
				SubElement(root, 'upnp:searchclass').text = i
		if self.searchable is not None:
			root.attrib['searchable'] = str(self.searchable)
		return root

	def __repr__(self):
		cls = self.__class__
		return '<%s.%s: id: %s, parent: %s, title: %s, cnt: %d>' % \
		    (cls.__module__, cls.__name__, self.id, self.parentID,
		    self.title, len(self))

class Person(Container):
	klass = Container.klass + '.person'

class MusicArtist(Person):
	klass = Person.klass + '.musicArtist'

class PlaylistContainer(Container):
	klass = Container.klass + '.playlistContainer'

class Album(Container):
	klass = Container.klass + '.album'

class MusicAlbum(Album):
	klass = Album.klass + '.musicAlbum'

class PhotoAlbum(Album):
	klass = Album.klass + '.photoAlbum'

class Genre(Container):
	klass = Container.klass + '.genre'

class MusicGenre(Genre):
	klass = Genre.klass + '.musicGenre'

class MovieGenre(Genre):
	klass = Genre.klass + '.movieGenre'

class StorageSystem(Container):
	klass = Container.klass + '.storageSystem'
	total = -1
	used = -1
	free = -1
	maxpartition = -1
	medium = 'UNKNOWN'

	def toElement(self):
		root = Container.toElement(self)
		SubElement(root, 'upnp:storageTotal').text = str(self.total)
		SubElement(root, 'upnp:storageUsed').text = str(self.used)
		SubElement(root, 'upnp:storageFree').text = str(self.free)
		SubElement(root, 'upnp:storageMaxPartition').text = str(self.maxpartition)
		SubElement(root, 'upnp:storageMedium').text = self.medium
		return root

class StorageVolume(Container):
	klass = Container.klass + '.storageVolume'
	total = -1
	used = -1
	free = -1
	medium = 'UNKNOWN'

	def toElement(self):
		root = Container.toElement(self)
		SubElement(root, 'upnp:storageTotal').text = str(self.total)
		SubElement(root, 'upnp:storageUsed').text = str(self.used)
		SubElement(root, 'upnp:storageFree').text = str(self.free)
		SubElement(root, 'upnp:storageMedium').text = self.medium
		return root

class StorageFolder(Container):
	klass = Container.klass + '.storageFolder'
	used = -1

	def toElement(self):
		root = Container.toElement(self)
		if self.used is not None:
			SubElement(root, 'upnp:storageUsed').text = str(self.used)
		return root

class DIDLElement(_ElementInterface):
	def __init__(self):
		_ElementInterface.__init__(self, 'DIDL-Lite', {})
		self.attrib['xmlns'] = 'urn:schemas-upnp-org:metadata-1-0/DIDL-Lite'
		self.attrib['xmlns:dc'] = 'http://purl.org/dc/elements/1.1/'
		self.attrib['xmlns:upnp'] = 'urn:schemas-upnp-org:metadata-1-0/upnp'

	def addContainer(self, P_id, parentID, title, restricted = False):
		e = Container(P_id, parentID, title, restricted, creator = '')
		self.append(e.toElement())

	def addItem(self, item):
		self.append(item.toElement())

	def numItems(self):
		return len(self)

	def toString(self):
		return tostring(self)

if __name__ == '__main__':

	root = DIDLElement()
	root.addContainer('0\Movie\\', '0\\', 'Movie')
	root.addContainer('0\Music\\', '0\\', 'Music')
	root.addContainer('0\Photo\\', '0\\', 'Photo')
	root.addContainer('0\OnlineMedia\\', '0\\', 'OnlineMedia')

	print(tostring(root))
