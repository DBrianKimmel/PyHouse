"""
@name:      /home/briank/workspace/PyHouse/src/Modules/Computer/Bridges/test/xml_bridges.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2017 by D. Brian Kimmel
@note:      Created on Dec 22, 2017
@license:   MIT License
@summary:

"""

__updated__ = '2017-12-22'

TESTING_BRIDGES_SECTION = 'BridgesSection'

L_BRIDGES_START = '<' + TESTING_BRIDGES_SECTION + '>'
L_BRIDGES_END = '</' + TESTING_BRIDGES_SECTION + '>'

XML_BRIDGES = '\n'.join([
    L_BRIDGES_START,
    L_BRIDGES_END
])

# ## END DBK
