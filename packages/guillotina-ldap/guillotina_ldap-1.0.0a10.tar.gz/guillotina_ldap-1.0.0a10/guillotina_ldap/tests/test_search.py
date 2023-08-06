from guillotina.component import get_utility
from guillotina_ldap.interfaces import ILDAPUsers
import pytest
import asyncio


@pytest.mark.parametrize("install_addons", [["email_validation"]])
@pytest.mark.asyncio
async def test_ldap_search(ldap, container_install_requester):
    await asyncio.sleep(4)
    async with container_install_requester as requester:
        # Add a user first
        util = get_utility(ILDAPUsers)
        async for user in util.search_user('anna'):
            assert user['fullname'] == 'Anna'
            assert user['id'] == 'anna'

        assert 'Anna' == await util.exists('anna')
