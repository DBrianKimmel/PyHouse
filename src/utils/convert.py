'''
Created on Apr 3, 2013

@author: briank

Utility routines to convert external readable numbers to integers for
ease in comparing.
'''

import unittest


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

class ConvertInsteon(object):
    """
    """

    def dotted_hex2long(self, p_addr):
        """Convert A1.B2.C3 to long
        """
        l_hexn = ''.join(["%02X" % int(l_ix, 16) for l_ix in p_addr.split('.')])
        return long(l_hexn, 16)

    def long2dotted_hex(self, p_long):
        """
        """
        l_ix = 256 * 256
        l_hex = []
        while l_ix > 0:
            l_byte, p_long = divmod(p_long, l_ix)
            l_hex.append("{0:02X}".format(l_byte))
            l_ix = l_ix / 256
        return '.'.join(l_hex)


class TestConvertions(unittest.TestCase):
    """
    """

    def setUp(self):
        self.eth = ConvertEthernet()
        self.inst = ConvertInsteon()

    def test_ethernet(self):
        t_dq = '192.168.1.65'
        t_long = 3232235841L
        l_long = self.eth.dotted_quad2long(t_dq)
        l_dq = self.eth.long2dotted_quad(t_long)
        self.assertEqual(t_long, l_long)
        self.assertEqual(t_dq, l_dq)
        # print l_long, l_dq

    def test_insteon(self):
        t_addr = 'A1.B2.C3'
        t_long = 10597059L
        l_long = self.inst.dotted_hex2long(t_addr)
        l_addr = self.inst.long2dotted_hex(t_long)
        self.assertEqual(t_long, l_long)
        self.assertEqual(t_addr, l_addr)
        # print l_long, l_addr


if __name__ == "__main__":
    print "running unittest.main()"
    unittest.main()
    # print "running TestConversions()"
    # TestConvertions()

# ## END
