"""
families.__init__.py

Various families of lighting systems.

insteon
upb
x-10
zigbee
z-wave
lutron
and others

To add a family named 'NewFamily', do the following:
    * Add a package named 'New_Family'.
    * Add the family name (Capitalized) to the list VALID_FAMILIES below.
    * Add a module named Device_<NewFamily>.py
    * Add any other modules needed by the Device module.
    * A module to interface with the controller is recommended.

There are a number of lighting 'Family' types handled here.
The Insteon family is now functional (2012).
The UPB family is work in progress
The X-10 family is mostly just a stub at present (2012)

Each family consists of four major areas:
    Lights / Lighting Devices
    Controllers - connected to the computer
    Scenes - have one or more lights that are controlled together
    Buttons - extra buttons with no light directly attached (key-pad-link)

"""

__version_info__ = (1, 0, 0)
__version__ = '.'.join(map(str, __version_info__))

VALID_FAMILIES = ['Insteon', 'UPB', 'X10']

#print "Running families now."
#
#import importlib
#
#for l_family in VALID_FAMILIES:
#    l_fqn = 'families.' + l_family + '.Device_' + l_family
#    l_pkg = 'src.families.' + l_family
#    l_mod = '.Device_' + l_family
#    try:
#        #l_module = importlib.import_module(l_fqn)
#        pass
#    except ImportError, l_err:
#        print "families() 1 - ImportError: :'{0:}', {1:}\n".format(l_fqn, l_err)
#    try:
#        l_module = importlib.import_module(l_mod, l_pkg)
#        pass
#    except ImportError, l_err:
#        print "families() 2 - ImportError: :'{0:}', {1:}, {2:}\n".format(l_mod, l_pkg, l_err)

# ## END DBK
