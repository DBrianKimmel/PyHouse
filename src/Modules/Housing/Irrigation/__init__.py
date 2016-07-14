"""
The irrigation system.

Each irrigation system has one source of water.  It could be a faucet or a dedicated line or a well with a pump.
The system can be always on, seasonally on (above freezing?) or use a pummp relay and/or master valve.

A system may be devided into zones.  Each zone can take a part or all of the water being used.
Within a system, only one zone may be active at a time.
"""

__version_info__ = (1, 6, 0)
__version__ = '.'.join(map(str, __version_info__))

# ## END DBK
