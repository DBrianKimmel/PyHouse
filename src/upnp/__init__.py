#
""" upnp/__init__.py

This package is based on Coherence and has been cut down a lot.
The intent is to be able to control other UPnP/DLNA devices and renderers
as well as lighting, HVAC devices and other home systems that can be
automated.

There is no attempt to be a media server.  That should be another completely
different process.

This is intended to control lighting as well as entertainment devices.
We should be able to schedule recordings of various media for later playback.
We should be able to record it on this computer or on another media server.
We should respond to other control points in turning on or off lights.

"""

__version_info__ = (1, 0, 2)
__version__ = '.' . join(map(str, __version_info__))



### END
