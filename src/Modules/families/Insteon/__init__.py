"""
# insteon/__init__.py

This interfaces PyHouse to the Insteon family of products.
This includes light switches, thermostats and a number of other devices.
"""

import sys

__version_info__ = (1, 0, 2)
__version__ = '.'.join(map(str, __version_info__))


# try:
#    from twisted import version as twisted_version
#    from twisted.web import version as twisted_web_version
#    from twisted.python.versions import Version
# except ImportError, exc:
#    # log error to stderr, might be useful for debugging purpose
#    sys.stderr.write("Twisted >= 2.5 and Twisted.Web >= 2.5 are required. "\
#                     "Please install them.\n")
#    raise

#
# import Device_Insteon
# import Insteon_PLM



"""
2014-07-02 09:52:23-0400 [PyHouse.Insteon_PLM ] decode_message() -  0x02 0x50 0x14 0x93 0x6f 0x00 0x00 0x01 0xc7 0x13 0x00 0x02 0x50 0x14 0x93 0x6f 0xaa 0xaa 0xaa 0x41 0x13 0x01 <END>
2014-07-02 09:52:23-0400 [PyHouse.Insteon_PLM ] Insteon_PLM.get_obj_from_message - Address:14.93.6F(1348463), found:**1348463**
2014-07-02 09:52:23-0400 [PyHouse.Insteon_PLM ] Insteon_PLM.get_obj_from_message - Address:00.00.01(1), found:**1**
2014-07-02 09:52:23-0400 [PyHouse.Insteon_PLM ] == 50B All-link Broadcast From:**1348463**, Group:1, Flags:All_Brdcst-Std-1-3=0XC7, Data:[19, 0] ==
2014-07-02 09:52:23-0400 [PyHouse.Insteon_PLM ] Standard Message; All-Link broadcast From:**1348463**, Group:1, Flags:All_Brdcst-Std-1-3=0XC7, Data:[19, 0];
2014-07-02 09:52:23-0400 [PyHouse.Insteon_PLM ] decode_message() -  0x02 0x50 0x14 0x93 0x6f 0xaa 0xaa 0xaa 0x41 0x13 0x01 <END>
2014-07-02 09:52:23-0400 [PyHouse.Insteon_PLM ] Insteon_PLM.get_obj_from_message - Address:14.93.6F(1348463), found:**1348463**
2014-07-02 09:52:23-0400 [PyHouse.Insteon_PLM ] Insteon_PLM.get_obj_from_message - Address:AA.AA.AA(11184810), found:PLM_1
2014-07-02 09:52:23-0400 [PyHouse.Insteon_PLM ] Standard Message; All-Link Broadcast clean up from **1348463**;

2014-07-02 09:52:23-0400 [PyHouse.Insteon_PLM ] decode_message() -  0x02 0x50 0x14 0x93 0x6f 0xaa 0xaa 0xaa 0x42 0x13 0x01 <END>
2014-07-02 09:52:23-0400 [PyHouse.Insteon_PLM ] Insteon_PLM.get_obj_from_message - Address:14.93.6F(1348463), found:**1348463**
2014-07-02 09:52:23-0400 [PyHouse.Insteon_PLM ] Insteon_PLM.get_obj_from_message - Address:AA.AA.AA(11184810), found:PLM_1
2014-07-02 09:52:23-0400 [PyHouse.Insteon_PLM ] Standard Message; All-Link Broadcast clean up from **1348463**;
2014-07-02 09:53:23-0400 [PyHouse.Insteon_PLM ] decode_message() -  0x02 0x50 0x14 0x93 0x6f 0xaa 0xaa 0xaa 0x07 0x6e 0x4e <END>
2014-07-02 09:53:23-0400 [PyHouse.Insteon_PLM ] Insteon_PLM.get_obj_from_message - Address:14.93.6F(1348463), found:**1348463**
2014-07-02 09:53:23-0400 [PyHouse.Insteon_PLM ] Insteon_PLM.get_obj_from_message - Address:AA.AA.AA(11184810), found:PLM_1
2014-07-02 09:53:23-0400 [PyHouse.Insteon_PLM ] Standard Message; DirectMessage from **1348463**;

"""

# ## END DBK
