"""
Created on Jul 11, 2013

@author: briank
"""
from zope.interface import Interface, Attribute

class IWebAccess(Interface):
    """
    An object with
    """

    def roomsList(p_house_obj):
        """
        Returns the pressure this material can support without
        fracturing at the given temperature.

        @type temperature: C{float}
        @param temperature: Kelvins

        @rtype: C{float}
        @return: Pascals
        """

    dielectricConstant = Attribute("""
        @type dielectricConstant: C{complex}
        @ivar dielectricConstant: The relative permittivity, with the
        real part giving reflective surface properties and the
        imaginary part giving the radio absorption coefficient.
        """)

# ## END DBK
