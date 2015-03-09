"""
@name: PyHouse/src/Modules/Computer/test/xml_computer.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@Copyright: (c)  2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Nov 8, 2014
@Summary:

"""

# Import system type stuff

# Import PyMh files
from Modules.Communication.test.xml_communications import *
from Modules.Computer.Internet.test.xml_internet import *
from Modules.Computer.Nodes.test.xml_nodes import *
from Modules.Web.test.xml_web import *



COMPUTER_DIVISION_XML = '\n'.join([
    "<ComputerDivision>",
    NODES_XML,
    COMMUNICATION_XML,
    WEB_SERVER_XML,
    INTERNET_XML,
    "</ComputerDivision>",
    ''
])




COMPUTER_XSD = """
"""

# ## END DBK