#!/usr/bin/env python
# Copyright 2006 John-Mark Gurney <jmg@funkthat.com>

__version__ = '$Change: 1227 $'
# $Id: //depot/python/pymeds/pymeds-0.5/FileDIDL.py#1 $

#
# Convert file information into a DIDL class.  Dynamicly generate a new class
# from a base class and the DIDL class to be determined.
#

__all__ = [ 'mimetoclass', 'buildClassMT', 'getClassMT', ]

import os.path
import weakref
from DIDLLite import VideoItem, AudioItem, TextItem, ImageItem
from twisted.python import log
from twisted.web import static

mimedict = static.loadMimeTypes()
classdict = weakref.WeakValueDictionary()

mimetoclass = {
	'application/ogg':	AudioItem,
	'video':		VideoItem,
	'audio':		AudioItem,
	'text':			TextItem,
	'image':		ImageItem,
}

def getClassMT(name, mimetype = None, fp = None):
	'''Return a tuple of the DIDLLite class and mimetype responsible for the named/mimetyped/fpd file.'''
	if mimetype is None:
		_fn, ext = os.path.splitext(name)
		ext = ext.lower()
		try:
			mimetype = mimedict[ext]
		except KeyError:
			log.msg('no mime-type for: %s' % name)
			return None, None

	ty = mimetype.split('/')[0]
	if mimetoclass.has_key(mimetype):
		klass = mimetoclass[mimetype]
	elif mimetoclass.has_key(ty):
		klass = mimetoclass[ty]
	else:
		# XXX - We could fall file -i on it
		log.msg('no item for mimetype: %s' % mimetype)
		return None, None

	return klass, mimetype

def buildClassMT(baseklass, name, *args, **kwargs):
	klass, mt = getClassMT(name, *args, **kwargs)

	if klass is None:
		return None, None

	try:
		return classdict[(baseklass, klass)], mt
	except KeyError:
		pass

	class ret(baseklass, klass):
		pass
	ret.__name__ = '+'.join(map(lambda x: '%s.%s' % (x.__module__, x.__name__), (baseklass, klass)))

	classdict[(baseklass, klass)] = ret

	return ret, mt
