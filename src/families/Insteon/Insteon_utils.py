'''
Created on Apr 27, 2013

@author: briank
'''

def message2int(self, p_message, p_index):
    """Extract the address from a message.

    The message is a byte array returned from the PLM.
    Return an int that is the address.
    """
    l_int = p_message[p_index] * 256 * 256 + p_message[p_index + 1] * 256 + p_message[p_index + 2]
    return l_int

def int2message(self, p_int, p_message, p_index):
    l_ix = 256 * 256
    while l_ix > 0:
        p_message[p_index], p_int = divmod(p_int, l_ix)
        l_ix = l_ix / 256
        p_index += 1
    return p_message

def dotted_hex2int(p_addr):
    """Convert A1.B2.C3 to int
    """
    l_hexn = ''.join(["%02X" % int(l_ix, 16) for l_ix in p_addr.split('.')])
    return int(l_hexn, 16)

def int2dotted_hex(p_int):
    """
    """
    l_ix = 256 * 256
    l_hex = []
    while l_ix > 0:
        l_byte, p_int = divmod(p_int, l_ix)
        l_hex.append("{0:02X}".format(l_byte))
        l_ix = l_ix / 256
    return '.'.join(l_hex)

# ## END DBK
