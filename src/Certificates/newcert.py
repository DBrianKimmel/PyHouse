"""
-*- test-case-name: PyHouse.src.Certificates.test.test_newcert -*-

@name:       PyHouse/src/Certificates/newcert.py
@author:     D. Brian Kimmel
@contact:    d.briankimmel@gmail.com
@copyright:  2015 by D. Brian Kimmel
@note:       Created on Feb 24, 2015
@license:    MIT License
@summary:

For posterity, you'll first need to generate a few client certificates all signed by the same CA.
You've probably already done this, but so others can understand the answer and try it out on their own
(and so I could test my answer myself ;-)), they'll need some code like this:

With this program, you can create a few certificates like so:
    $ python newcert.py a
    $ python newcert.py b

"""

from twisted.python.filepath import FilePath
from twisted.internet.ssl import PrivateCertificate, KeyPair, DN


def getCAPrivateCert():
    l_privatePath = FilePath(b"ca-private-cert.pem")
    if l_privatePath.exists():
        return PrivateCertificate.loadPEM(l_privatePath.getContent())
    else:
        l_caKey = KeyPair.generate(size = 4096)
        l_caCert = l_caKey.selfSignedCert(1, CN = "the-authority")
        l_privatePath.setContent(l_caCert.dumpPEM())
        return l_caCert

def clientCertFor(p_name):
    l_signingCert = getCAPrivateCert()
    l_clientKey = KeyPair.generate(size = 4096)
    l_csr = l_clientKey.requestObject(DN(CN = p_name), "sha1")
    l_clientCert = l_signingCert.signRequestObject(
        l_csr, serialNumber = 1, digestAlgorithm = "sha1")
    return PrivateCertificate.fromCertificateAndKeyPair(l_clientCert, l_clientKey)


if __name__ == '__main__':
    import sys
    l_name = sys.argv[1]
    l_pem = clientCertFor(l_name.encode("utf-8")).dumpPEM()
    FilePath(l_name.encode("utf-8") + b".client.private.pem").setContent(l_pem)

# ## END DBK
