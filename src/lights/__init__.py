"""
# lighting/__init__.py

When adding a family of lighting devices:
    * Create a new package named like 'insteon'
    * Create a module in that package named like 'Device_Insteon'
    * Create other modules as needed.
    * Add family name to VALID_FAMILIES in lighting.py

"""

import sys

__version_info__ = (1, 1, 0)
__version__ = '.'.join(map(str, __version_info__))

# ## END DBK
