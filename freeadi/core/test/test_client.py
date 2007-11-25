#
# This file is part of FreeADI. FreeADI is free software that is made
# available under the MIT license. Consult the file "LICENSE" that is
# distributed together with this file for the exact licensing terms.
#
# FreeADI is copyright (c) 2007 by the FreeADI authors. See the file
# "AUTHORS" for a complete overview.

from freeadi.test.base import BaseTest
from freeadi.core.client import Client as ADClient


class TestADClient(BaseTest):
    """Test suite for ADClient"""

    def test_simple(self):
        self.require(ad_user=True)
