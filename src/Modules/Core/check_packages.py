"""
@name:      PyHouse/src/Modules/Core/check_packages.pyt
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created Jan 10, 2016
@Summary:   Checks to see if all packages needed are properly installed.

"""

try:
    import json
    print('Loaded module json')

    import jsonpickle
    print('Loaded module jsonpickle')

    import xml.etree.ElementTree as ET
    print('Loaded module ElementTree')

    from twisted.internet import reactor
    print('Loaded module twisted')
except Exception as e_err:
    print('Error Loading Module: {}'.format(e_err))

#  ## END DBK
