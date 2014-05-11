"""
Created on Apr 3, 2013

@author: briank

Utility routines to convert external readable numbers to integers for
ease in comparing.
"""


class ConvertEthernet(object):
    '''
    Handle Ethernet V-4 32 bit numbers
    '192.168.1.65' != 3232235841L
    '''


    def dotted_quad2long(self, p_quad):
        """convert decimal dotted quad string to long integer
        """
        l_hexn = ''.join(["%02X" % long(i) for i in p_quad.split('.')])
        return long(l_hexn, 16)

    def long2dotted_quad(self, p_long):
        """convert long int to dotted quad string
        """
        d = 256 * 256 * 256
        q = []
        while d > 0:
            m, p_long = divmod(p_long, d)
            q.append(str(m))
            d = d / 256
        return '.'.join(q)

def v4_to_int(p_v4):
    l_sum = 0
    l_mul = 1
    for l_part in reversed(p_v4.split(".")):
        l_sum += int(l_part) * l_mul
        l_mul *= 2 ** 8
    return l_sum


# ## END DBK
