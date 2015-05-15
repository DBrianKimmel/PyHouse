"""Developer documentation.

Most of the developer documentation is in each package __init__.py module.

Requirements:
    Python 2.7.x                (2.7.3-4+deb7u1)         (Waiting for twisted to support Python 3.x)
    python-setuptools           (0.6.24-1)
    python-twisted              (14.0.0-1)
    python-nevow                (0.10.0-4)
    python-dev                  (2.7.3-4+deb7u1)
    python-dateutil             (1.5+dfsg-0.1)
    python-netaddr              (0.7.7-1)
    python-usb                  (0.4.3-1)
    python-jsonpickle           (0.4.0-1)
    python-netifaces            (0.8-1)
    python-openssl              (0.13-2+rpi1+deb7u1)
    python-serial               (2.5-2.1)

    libevent-dev
    service_identity



Windows:
    pip install dateutils
    pip install netaddr
    pip install netifaces
    pip install pyusb
    pip install jsonpickle
    pip install passlib
    pip install pyopenSSL
    pip install paho-mqtt        (Windows linux)




Overall documentation.

Each module will most likely contain an 'API' class.  The constructor for
this class will give a reference address for the module.

The 'Start' method, if any,  will read any XML and set up the data for this
module.  It will also call any other modules that it will need.

The 'Stop' method, if any, will write any XML file to update it.  It will also
close down any thing it no longer needs so they can be cleanly reloaded.

In order to keep the API class clean, modules may have a 'Utilities'
class.  The API class will inherit from this class so that its
methods may be accessible by other modules.

The PyHouse module created a data structure that is passed to some
high level modules.


PyHouse is a Twisted Python Application - See twisted.application
It runs a number of "services" within that application (e.g. web service)
"""

__version_info__ = (1, 1, 0)
__version__ = '.'.join(map(str, __version_info__))

# ## END DBK
