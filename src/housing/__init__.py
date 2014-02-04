"""
Housing package documentation.

The houseing package allows more than one house to be in the XML file
at a time.  We live in two different houses and take the development
computer back and forth between them.  Having several houses in the
XML file keeps the data from the previous year intact.  In addition,
I can add a test house to the houses and do development testing without
disturbing the real house information.

The houses (plural) module is a singleton and loads a house module for each
house in the XML file.  All houses are loaded whether active or not.
The entire XML file is eventually loaded and when a save point is
encountered, the entire XML file is updated with the updated information.

The house (singular) module is instantiated once for every house in the XML
configuration file.  Each house runs its own schedule, has its own
location, lights, controllers and room list.

TODO:
Each house can draw itself on a canvas and show lights in the proper
rooms with their proper current status.
"""

__version_info__ = (1, 1, 0)
__version__ = '.'.join(map(str, __version_info__))

# ## END DBK
