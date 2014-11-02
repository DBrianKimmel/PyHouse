"""
hvac.__init__.py

This is the interface from HVAC to PyHouse.

"""

__version_info__ = (1, 1, 0)
__version__ = '.'.join(map(str, __version_info__))

VALID_TEMP_SYSTEMS = ['C', 'F']
VALID_THERMOSTAT_MODES = ['Heat', 'Cool', 'Auto', 'EHeat']

# ## END
