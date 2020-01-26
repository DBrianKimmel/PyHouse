"""

__updated__ = '2020-01-24'
__version_info__ = (20, 1, 24)
__version__ = '.'.join(map(str, __version_info__))

"""


class NodeInformation:
    """ Information about a single node.
    Name is the Node's HostName
    The interface info is only for the local node.

    ==> PyHouse.Computer.Nodes[x].xxx - as in the def below.
    """

    def __init__(self):
        self.Name = None
        self.Comment = None
        self.NodeRole = None
        self.NodeInterfaces = {}  # NodeInterfaceData()

# ## END DBK
