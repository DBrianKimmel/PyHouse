#!/usr/bin/env python
# Copyright 2006-2008 John-Mark Gurney <jmg@funkthat.com>

__version__ = '$Change: 1227 $'
# $Id: //depot/python/pymeds/pymeds-0.5/FSStorage.py#1 $

ffmpeg_path = '/usr/local/bin/ffmpeg'

import UPnP_FileDIDL
import errno
import itertools
import os
import sets
import stat

from UPnP_DIDLLite import Container, StorageFolder, Item, VideoItem, AudioItem, TextItem, ImageItem, Resource, ResourceList
from twisted.web import resource, server, static
from twisted.python import log
from twisted.internet import abstract
from twisted.internet import interfaces
#from twisted.internet import process
from twisted.internet import protocol
from twisted.internet import reactor
from zope.interface import implements

__all__ = [ 'registerklassfun', 'registerfiletoignore',
		'FSObject', 'FSItem', 'FSDirectory',
		'FSVideoItem', 'FSAudioItem', 'FSTextItem', 'FSImageItem',
		'mimetoklass',
	]

mimedict = static.loadMimeTypes()

_klassfuns = []

def registerklassfun(fun):
	_klassfuns.append(fun)

_filestoignore = {
		'.DS_Store': None
	}

def registerfiletoignore(f):
	_filestoignore[f] = None

# Return this class when you want the file to be skipped.  If you return this,
# no other modules will be applied, and it won't be added.  Useful for things
# like .DS_Store which are known to useless on a media server.
class IgnoreFile:
	pass

def statcmp(a, b, cmpattrs = [ 'st_ino', 'st_dev', 'st_size', 'st_mtime', ]):
	if a is None or b is None:
		return False

	for i in cmpattrs:
		if getattr(a, i) != getattr(b, i):
			return False
	return True

class FSObject(object):
	def __init__(self, path):
		self.FSpath = path
		self.pstat = None

	def checkUpdate(self):
		# need to handle no such file or directory
		# push it up? but still need to handle disappearing
		try:
			nstat = os.stat(self.FSpath)
			if statcmp(self.pstat, nstat):
				return self

			self.pstat = nstat
			self.doUpdate()
		except OSError, x:
			log.msg('os.stat, OSError: %s' % x)
			if x.errno in (errno.ENOENT, errno.ENOTDIR, errno.EPERM, ):
				# We can't access it anymore, delete it
				self.cd.delItem(self.id)
				return None
			else:
				raise

		return self

	def doUpdate(self):
		raise NotImplementedError


	def __repr__(self):
		return '<%s.%s: path: %s, id: %s, parent: %s, title: %s>' % \
		    (self.__class__.__module__, self.__class__.__name__,
		    self.FSpath, self.id, self.parentID, self.title)

class NullConsumer(file, abstract.FileDescriptor):
	implements(interfaces.IConsumer)

	def __init__(self):
		file.__init__(self, '/dev/null', 'w')
		abstract.FileDescriptor.__init__(self)

	def write(self, data):
		pass

class DynamTransfer(protocol.ProcessProtocol):
	def __init__(self, path, mods, request):
		self.path = path
		self.mods = mods
		self.request = request

	def outReceived(self, data):
		self.request.write(data)

	def outConnectionLost(self):
		if self.request:
			self.request.unregisterProducer()
			self.request.finish()
			self.request = None

	def errReceived(self, data):
		pass
		#log.msg(data)

	def stopProducing(self):
		if self.request:
			self.request.unregisterProducer()
			self.request.finish()

		if self.proc:
			self.proc.loseConnection()
			self.proc.signalProcess('INT')

		self.request = None
		self.proc = None

	pauseProducing = lambda x: x.proc.pauseProducing()
	resumeProducing = lambda x: x.proc.resumeProducing()

	def render(self):
		mods = self.mods
		path = self.path
		request = self.request

		vcodec = mods[0]
		if mods[0] not in ('xvid', 'mpeg2', ):
			vcodec = 'xvid'

		mimetype = { 'xvid': 'video/avi', 'mpeg2': 'video/mpeg', }
		mimetype = { 'xvid': 'video/x-msvideo', 'mpeg2': 'video/mpeg', }
		request.setHeader('content-type', mimetype[vcodec])
		if request.method == 'HEAD':
			return ''

		audiomp3 = [ '-acodec', 'mp3', '-ab', '192', ]
		audiomp2 = [ '-acodec', 'mp2', '-ab', '256', ]
		optdict = {
			'xvid':	[ '-vcodec', 'xvid',
				  #'-mv4', '-gmc', '-g', '240',
				  '-f', 'avi', ] + audiomp3,
			'mpeg2': [ '-vcodec', 'mpeg2video', #'-g', '60',
				   '-f', 'mpeg', ] + audiomp2,
			}
		args = [ 'ffmpeg', '-i', path, '-b', '4000',
		    #'-sc_threshold', '500000', '-b_strategy', '1', '-max_b_frames', '6',
			] + optdict[vcodec] + [ '-', ]
		#log.msg(*[`i` for i in args])
		self.proc = process.Process(reactor, ffmpeg_path, args,
		    None, None, self)
		self.proc.closeStdin()
		request.registerProducer(self, 1)

		return server.NOT_DONE_YET

class DynamicTrans(resource.Resource):
	isLeaf = True

	def __init__(self, path, notrans):
		self.path = path
		self.notrans = notrans

	def render(self, request):
		#if request.getHeader('getcontentfeatures.dlna.org'):
		#	request.setHeader('contentFeatures.dlna.org', 'DLNA.ORG_OP=01;DLNA.ORG_CI=0')
		#	# we only want the headers
		#	self.notrans.render(request)
		#	request.unregisterProducer()  
		#	return ''

		if request.postpath:
			# Translation request
			return DynamTransfer(self.path, request.postpath, request).render()
		else:
			return self.notrans.render(request)

class FSItem(FSObject, Item):
	def __init__(self, *args, **kwargs):
		FSObject.__init__(self, kwargs['path'])
		del kwargs['path']
		mimetype = kwargs['mimetype']
		del kwargs['mimetype']
		kwargs['content'] = DynamicTrans(self.FSpath,
		    static.File(self.FSpath, mimetype))
		Item.__init__(self, *args, **kwargs)
		self.url = '%s/%s' % (self.cd.urlbase, self.id)
		self.mimetype = mimetype
		self.checkUpdate()

	def doUpdate(self):
		#print 'FSItem doUpdate:', `self`
		self.res = ResourceList()
		r = Resource(self.url, 'http-get:*:%s:*' % self.mimetype)
		r.size = os.path.getsize(self.FSpath)
		self.res.append(r)
		if self.mimetype.split('/', 1)[0] == 'video':
			self.res.append(Resource(self.url + '/mpeg2',
			    'http-get:*:%s:*' % 'video/mpeg'))
			self.res.append(Resource(self.url + '/xvid',
			    'http-get:*:%s:*' % 'video/x-msvideo'))
		Item.doUpdate(self)

def ignoreFiles(path, fobj):
	if os.path.basename(path) in _filestoignore:
		return IgnoreFile, None

	return None, None

def defFS(path, fobj):
	if os.path.isdir(path):
		# new dir
		return FSDirectory, { 'path': path }
	elif os.path.isfile(path):
		# new file - fall through to below
		pass
	else:
		log.msg('skipping (not dir or reg): %s' % path)
		return None, None

	klass, mt = FileDIDL.buildClassMT(FSItem, path)

	return klass, { 'path': path, 'mimetype': mt }

def dofileadd(cd, parent, path, name):
	klass = None
	fsname = os.path.join(path, name)
	try:
		fobj = open(fsname)
	except:
		fobj = None
	for i in itertools.chain(( ignoreFiles, ), _klassfuns, ( defFS, )):
		try:
			try:
				fobj.seek(0)	# incase the call expects a clean file
			except:
				pass

			#log.msg('testing:', `i`, `fsname`, `fobj`)
			klass, kwargs = i(fsname, fobj)
			if klass is not None:
				break
		except:
			#import traceback
			#traceback.print_exc(file=log.logfile)
			pass

	if klass is None or klass is IgnoreFile:
		return

	#print 'matched:', os.path.join(path, name), `i`, `klass`
	return cd.addItem(parent, klass, name, **kwargs)

class FSDirectory(FSObject, StorageFolder):
        """Class to be imported.
        """
	def __init__(self, *args, **kwargs):
		path = kwargs['path']
		del kwargs['path']
		StorageFolder.__init__(self, *args, **kwargs)
		FSObject.__init__(self, path)
		# mapping from path to objectID
		self.pathObjmap = {}
		self.indoUpdate = False

	def doUpdate(self):
		# We need to rescan this dir, and see if our children has
		# changed any.
		if self.indoUpdate:
			return
		#import traceback
		#traceback.print_stack()
		self.indoUpdate = True
		doupdate = False
		children = sets.Set(os.listdir(self.FSpath))
		for i in self.pathObjmap.keys():
			if i not in children:
				doupdate = True
				# delete
				self.cd.delItem(self.pathObjmap[i])
				del self.pathObjmap[i]
		for i in children:
			if i in self.pathObjmap:
				continue
			# new object
			nf = dofileadd(self.cd, self.id, self.FSpath, i)
			if nf is not None:
				doupdate = True
				self.pathObjmap[i] = nf
		# sort our children
		self.sort(lambda x, y: cmp(x.title, y.title))
		# Pass up to handle UpdateID
		if doupdate:
			# Calling StorageFolder.doUpdate results in calling
			# ourselves.
			Container.doUpdate(self)
		self.indoUpdate = False

	def __repr__(self):
		return ('<%s.%s: path: %s, id: %s, parent: %s, title: %s, ' + \
		    'cnt: %d>') % (self.__class__.__module__,
		    self.__class__.__name__, self.FSpath, self.id,
		    self.parentID, self.title, len(self))
