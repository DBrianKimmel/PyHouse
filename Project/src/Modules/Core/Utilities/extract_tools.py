"""
-*- test-case-name: /home/briank/workspace/PyHouse/Project/src/Modules/Core/Utilities/extract_tools.py -*-

@name:      /home/briank/workspace/PyHouse/Project/src/Modules/Core/Utilities/extract_tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2018-2018 by D. Brian Kimmel
@note:      Created on Oct 3, 2018
@license:   MIT License
@summary:

"""

__updated__ = '2018-10-05'

# Import system type stuff
from operator import index


def extract_quoted(p_string, p_delim=b'"'):
    """
    Discard characters before first p_delim
    extract chars between p_delim chars
    return all chars after second p_delim
    """
    l_string = p_string
    l_1st = l_string.find(p_delim)
    l_2nd = l_string.find(p_delim, l_1st + 1)
    l_string = p_string[l_1st + 1:l_2nd].decode('utf-8')
    l_rest = p_string[l_2nd + 1:]
    return l_string, l_rest

# ## END DBK
