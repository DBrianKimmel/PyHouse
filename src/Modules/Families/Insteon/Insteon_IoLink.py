"""
-*- test-case-name: /home/briank/PyHouse/src/Modules/Families/Insteon/Insteon_IoLink.py -*-

@name:      /home/briank/PyHouse/src/Modules/Families/Insteon/Insteon_IoLink.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2016-2016 by D. Brian Kimmel
@note:      Created on Sep 18, 2016
@license:   MIT License
@summary:   Handle the I/O Link module.

"""

__updated__ = '2016-09-30'



# ## END DBK

"""
2016-09-30 09:44:44,700 [INFO] PyHouse.Insteon_decode : decode_message 70: -  0x02 0x50 0x3d 0xe3 0xec 0x00 0x00 0x01 0xc7 0x11 0x00 0x02 0x50 0x3d 0xe3 0xec 0x34 0x77 0xf9 0x41 0x11 0x01 <END>
2016-09-30 09:44:44,702 [INFO] PyHouse.Insteon_decode : _decode_50_record 169: - == 50B All-link Broadcast Group:1, Data:[17, 0] ==
2016-09-30 09:44:44,713 [INFO] PyHouse.Insteon_decode : _decode_50_record 215: - 50 Resp; Std Msg fm: GDO; Cmd1:0x11, Cmd2:0x0; All-Link broadcast - Group:1, Data:[17, 0]; Device:GDO turned Full ON  ;
2016-09-30 09:44:44,714 [INFO] PyHouse.Insteon_decode : decode_message 70: -  0x02 0x50 0x3d 0xe3 0xec 0x34 0x77 0xf9 0x41 0x11 0x01 <END>
2016-09-30 09:44:44,725 [INFO] PyHouse.Insteon_decode : _decode_50_record 215: - 50 Resp; Std Msg fm: GDO; Cmd1:0x11, Cmd2:0x1; Device:GDO turned Full ON  ;
2016-09-30 09:44:45,300 [INFO] PyHouse.Insteon_decode : decode_message 70: -  0x02 0x50 0x3d 0xe3 0xec 0x34 0x77 0xf9 0x4b 0x11 0x01 <END>
2016-09-30 09:44:45,311 [INFO] PyHouse.Insteon_decode : _decode_50_record 215: - 50 Resp; Std Msg fm: GDO; Cmd1:0x11, Cmd2:0x1; Device:GDO turned Full ON  ;
2016-09-30 09:44:45,900 [INFO] PyHouse.Insteon_decode : decode_message 70: -  0x02 0x50 0x3d 0xe3 0xec 0x34 0x77 0xf9 0x4b 0x11 0x01 0x02 0x50 0x3d 0xe3 0xec 0x34 0x77 0xf9 0x4b 0x11 0x01 <END>
2016-09-30 09:44:45,910 [INFO] PyHouse.Insteon_decode : _decode_50_record 215: - 50 Resp; Std Msg fm: GDO; Cmd1:0x11, Cmd2:0x1; Device:GDO turned Full ON  ;
2016-09-30 09:44:45,911 [INFO] PyHouse.Insteon_decode : decode_message 70: -  0x02 0x50 0x3d 0xe3 0xec 0x34 0x77 0xf9 0x4b 0x11 0x01 <END>
2016-09-30 09:44:45,921 [INFO] PyHouse.Insteon_decode : _decode_50_record 215: - 50 Resp; Std Msg fm: GDO; Cmd1:0x11, Cmd2:0x1; Device:GDO turned Full ON  ;
2016-09-30 09:44:46,500 [INFO] PyHouse.Insteon_decode : decode_message 70: -  0x02 0x50 0x3d 0xe3 0xec 0x34 0x77 0xf9 0x41 0x11 0x01 <END>
2016-09-30 09:44:46,510 [INFO] PyHouse.Insteon_decode : _decode_50_record 215: - 50 Resp; Std Msg fm: GDO; Cmd1:0x11, Cmd2:0x1; Device:GDO turned Full ON  ;
2016-09-30 09:44:47,101 [INFO] PyHouse.Insteon_decode : decode_message 70: -  0x02 0x50 0x3d 0xe3 0xec 0x34 0x77 0xf9 0x46 0x11 0x01 0x02 0x50 0x3d 0xe3 0xec 0x34 0x77 0xf9 0x4b 0x11 0x01 <END>
2016-09-30 09:44:47,111 [INFO] PyHouse.Insteon_decode : _decode_50_record 215: - 50 Resp; Std Msg fm: GDO; Cmd1:0x11, Cmd2:0x1; Device:GDO turned Full ON  ;
2016-09-30 09:44:47,112 [INFO] PyHouse.Insteon_decode : decode_message 70: -  0x02 0x50 0x3d 0xe3 0xec 0x34 0x77 0xf9 0x4b 0x11 0x01 <END>
2016-09-30 09:44:47,121 [INFO] PyHouse.Insteon_decode : _decode_50_record 215: - 50 Resp; Std Msg fm: GDO; Cmd1:0x11, Cmd2:0x1; Device:GDO turned Full ON  ;
2016-09-30 09:44:47,701 [INFO] PyHouse.Insteon_decode : decode_message 70: -  0x02 0x50 0x3d 0xe3 0xec 0x34 0x77 0xf9 0x4b 0x11 0x01 <END>
2016-09-30 09:44:47,711 [INFO] PyHouse.Insteon_decode : _decode_50_record 215: - 50 Resp; Std Msg fm: GDO; Cmd1:0x11, Cmd2:0x1; Device:GDO turned Full ON  ;

2016-09-30 09:46:54,341 [INFO] PyHouse.Insteon_decode : decode_message 70: -  0x02 0x50 0x3d 0xe3 0xec 0x34 0x77 0xf9 0x41 0x13 0x01 0x02 0x50 0x3d 0xe3 0xec 0x34 0x77 0xf9 0x46 0x13 0x01 <END>
2016-09-30 09:46:54,353 [INFO] PyHouse.Insteon_decode : _decode_50_record 215: - 50 Resp; Std Msg fm: GDO; Cmd1:0x13, Cmd2:0x1; Light:GDO turned Full OFF;
2016-09-30 09:46:54,354 [INFO] PyHouse.Insteon_decode : decode_message 70: -  0x02 0x50 0x3d 0xe3 0xec 0x34 0x77 0xf9 0x46 0x13 0x01 <END>
2016-09-30 09:46:54,365 [INFO] PyHouse.Insteon_decode : _decode_50_record 215: - 50 Resp; Std Msg fm: GDO; Cmd1:0x13, Cmd2:0x1; Light:GDO turned Full OFF;
2016-09-30 09:46:54,942 [INFO] PyHouse.Insteon_decode : decode_message 70: -  0x02 0x50 0x3d 0xe3 0xec 0x34 0x77 0xf9 0x4b 0x13 0x01 <END>
2016-09-30 09:46:54,953 [INFO] PyHouse.Insteon_decode : _decode_50_record 215: - 50 Resp; Std Msg fm: GDO; Cmd1:0x13, Cmd2:0x1; Light:GDO turned Full OFF;
2016-09-30 09:46:55,542 [INFO] PyHouse.Insteon_decode : decode_message 70: -  0x02 0x50 0x3d 0xe3 0xec 0x34 0x77 0xf9 0x4b 0x13 0x01 <END>
2016-09-30 09:46:55,552 [INFO] PyHouse.Insteon_decode : _decode_50_record 215: - 50 Resp; Std Msg fm: GDO; Cmd1:0x13, Cmd2:0x1; Light:GDO turned Full OFF;
2016-09-30 09:46:56,142 [INFO] PyHouse.Insteon_decode : decode_message 70: -  0x02 0x50 0x3d 0xe3 0xec 0x34 0x77 0xf9 0x47 0x13 0x01 0x02 0x50 0x3d 0xe3 0xec 0x34 0x77 0xf9 0x41 0x13 0x01 <END>
2016-09-30 09:46:56,152 [INFO] PyHouse.Insteon_decode : _decode_50_record 215: - 50 Resp; Std Msg fm: GDO; Cmd1:0x13, Cmd2:0x1; Light:GDO turned Full OFF;
2016-09-30 09:46:56,153 [INFO] PyHouse.Insteon_decode : decode_message 70: -  0x02 0x50 0x3d 0xe3 0xec 0x34 0x77 0xf9 0x41 0x13 0x01 <END>
2016-09-30 09:46:56,163 [INFO] PyHouse.Insteon_decode : _decode_50_record 215: - 50 Resp; Std Msg fm: GDO; Cmd1:0x13, Cmd2:0x1; Light:GDO turned Full OFF;
2016-09-30 09:46:56,742 [INFO] PyHouse.Insteon_decode : decode_message 70: -  0x02 0x50 0x3d 0xe3 0xec 0x34 0x77 0xf9 0x46 0x13 0x01 0x02 0x50 0x3d 0xe3 0xec 0x34 0x77 0xf9 0x4b 0x13 0x01 <END>
2016-09-30 09:46:56,752 [INFO] PyHouse.Insteon_decode : _decode_50_record 215: - 50 Resp; Std Msg fm: GDO; Cmd1:0x13, Cmd2:0x1; Light:GDO turned Full OFF;
2016-09-30 09:46:56,753 [INFO] PyHouse.Insteon_decode : decode_message 70: -  0x02 0x50 0x3d 0xe3 0xec 0x34 0x77 0xf9 0x4b 0x13 0x01 <END>
2016-09-30 09:46:56,763 [INFO] PyHouse.Insteon_decode : _decode_50_record 215: - 50 Resp; Std Msg fm: GDO; Cmd1:0x13, Cmd2:0x1; Light:GDO turned Full OFF;
2016-09-30 09:46:57,342 [INFO] PyHouse.Insteon_decode : decode_message 70: -  0x02 0x50 0x3d 0xe3 0xec 0x34 0x77 0xf9 0x4b 0x13 0x01 <END>
2016-09-30 09:46:57,352 [INFO] PyHouse.Insteon_decode : _decode_50_record 215: - 50 Resp; Std Msg fm: GDO; Cmd1:0x13, Cmd2:0x1; Light:GDO turned Full OFF;
"""
