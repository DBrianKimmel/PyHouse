"""The house package contains modules ans sub-packages that operate on a single house.

The 'house' module is instantiated once for every house in the configuration file.
Each house runs its own schedule, has its own location, lights, controllers and room list.

Each house can draw itself on a canvas and show lights in the proper rooms with their
proper current status.
"""

__version_info__ = (1, 0, 0)
__version__ = '.'.join(map(str, __version_info__))


# ## END
