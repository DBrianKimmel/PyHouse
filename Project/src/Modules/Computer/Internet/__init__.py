"""
The internet package finds the connection to the public Internet.

It determines the IPv4 address of the interface to the ISP since the ISP usually NATs the address.
It will then take that IP address and update our Dynamic DNS provider(s) so we may browse to that
address from some external device and check on the status of the house.

It sends alerts if the address has changed.


All nodes currently run this.  This is overkill!
We need a way to have only one of the nodes run this package and if successful, block the other nodes from running it.

Get the internet address and make reports available for web interface.

Since PyHouse is always running (as a daemon) this package will get the IPv4 address that is
assigned to our router by the ISP.

"""
__updated__ = '2016-10-22'
__version_info__ = (1, 7, 4)
__version__ = '.'.join(map(str, __version_info__))

# ## END DBK
