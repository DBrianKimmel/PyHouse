"""The housus (plural) module allows more than one house in the XML file
at a time.  We live in two different houses and take the development
computer back and forth between them.  Having several houses in the
XML file keeps the data from the previous year intact.  In addition,
I can add a test house to the houses and do development testing without
disturbing the real house information.

The houses module is a singleton and loads a house module for each
house in the XML file.  All houses are loaded whether active or not.
The entire xml file is eventually loaded and when a save point is
encountered, the entire XML file is updated with the read in
information.

The house package contains modules and sub-packages that operate on a
single house.

The 'house' module is instantiated once for every house in the XML
configuration file.  Each house runs its own schedule, has its own
location, lights, controllers and room list.

Each house can draw itself on a canvas and show lights in the proper
rooms with their proper current status.
"""

__version_info__ = (1, 1, 0)
__version__ = '.'.join(map(str, __version_info__))

# ## END DBK
