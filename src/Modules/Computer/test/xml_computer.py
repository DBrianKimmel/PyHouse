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
from Modules.Communication.test.xml_communications import COMMUNICATION_XML
from Modules.Computer.Internet.test.xml_internet import INTERNET_XML
from Modules.Computer.Nodes.test.xml_nodes import NODES_XML
from Modules.Web.test.xml_web import WEB_SERVER_XML



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