"""
The irrigation system.

Each irrigation system has one source of water.  It could be a faucet or a dedicated line or a well with a pump.
The system can be always on, seasonally on (above freezing?) or use a pump relay and/or master valve.

A system may be divided into zones.  Each zone can take a part or all of the water being used.
Within a system, only one zone may be active at a time.

System Types:
    Multi Zoned.  This takes a pump-start relay or a master valve and then individual zone valves where the zones
    run in sequence.

    Single Zone.  This has a valve to turn the system on or off.
"""

__updated__ = '2020-01-25'

__version_info__ = (20, 1, 25)
__version__ = '.'.join(map(str, __version_info__))

VALID_IRRIGATION_TYPE = ['Multi', 'Single']

MODULES = [  # All modules for the House must be listed here.  They will be loaded if configured.
    'RainBird'
    ]


class IrrigationInformation:
    """ Info about any/all irrigation systems for a house.

    ==> PyHouse.House.Irrigation.xxx as in the def below
    """

    def __init__(self):
        self.Name = None
        self.Systems = {}  # IrrigationSystemData()

# ## END DBK
