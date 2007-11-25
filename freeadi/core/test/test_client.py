#
# This file is part of FreeADI. FreeADI is free software that is made
# available under the MIT license. Consult the file "LICENSE" that is
# distributed together with this file for the exact licensing terms.
#
# FreeADI is copyright (c) 2007 by the FreeADI authors. See the file
# "AUTHORS" for a complete overview.

from freeadi.test.base import BaseTest
from freeadi.core.object import activate
from freeadi.core.client import Client
from freeadi.core import client as ad
from freeadi.core.creds import Creds
from freeadi.core.exception import Error as ADError, LDAPError


class TestADClient(BaseTest):
    """Test suite for ADClient"""

    def test_search(self):
        self.require(ad_user=True)
        domain = self.domain()
        creds = Creds(domain)
        creds.acquire(self.ad_user_account(), self.ad_user_password())
        activate(creds)
        client = Client(domain)
        result = client.search('(objectClass=user)')
        assert len(result) > 1

    def _add_user(self, client, name):
        attrs = []
        attrs.append(('cn', ['freeadi']))
        attrs.append(('sAMAccountName', [name]))
        attrs.append(('userPrincipalName', ['%s@%s' % (name, client.domain().upper())]))
        ctrl = ad.CTRL_ACCOUNT_DISABLED | ad.CTRL_NORMAL_ACCOUNT
        attrs.append(('userAccountControl', [str(ctrl)]))
        attrs.append(('objectClass', ['user']))
        dn = 'cn=freeadi,cn=users,' + client.dn_from_domain_name(client.domain())
        try:
            client.delete(dn)
        except (ADError, LDAPError):
            pass
        client.add(dn, attrs)
        return dn

    def test_add_user(self):
        self.require(ad_admin=True)
        domain = self.domain()
        creds = Creds(domain)
        creds.acquire(self.ad_admin_account(), self.ad_admin_password())
        activate(creds)
        client = Client(domain)
        self._add_user(client, 'freeadi')

    def test_delete_user(self):
        self.require(ad_admin=True)
        domain = self.domain()
        creds = Creds(domain)
        creds.acquire(self.ad_admin_account(), self.ad_admin_password())
        activate(creds)
        client = Client(domain)
        dn = self._add_user(client, 'freeadi')
        client.delete(dn)

    def test_contexts(self):
        self.require(ad_user=True)
        domain = self.domain()
        creds = Creds(domain)
        creds.acquire(self.ad_user_account(), self.ad_user_password())
        activate(creds)
        client = Client(domain)
        contexts = client.contexts()
        assert len(contexts) >= 3

    def test_search_all_contexts(self):
        self.require(ad_user=True)
        domain = self.domain()
        creds = Creds(domain)
        creds.acquire(self.ad_user_account(), self.ad_user_password())
        activate(creds)
        client = Client(domain)
        contexts = client.contexts()
        for ctx in contexts:
            result = client.search('(objectClass=*)', scope=ad.SCOPE_BASE)
            assert len(result) == 1
