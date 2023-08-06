from guillotina.component import get_utility
from guillotina_ldap.interfaces import ILDAPUsers
import pytest
import asyncio


@pytest.mark.parametrize("install_addons", [["email_validation"]])
@pytest.mark.asyncio
async def test_ldap_add_exist(ldap, container_install_requester):
    await asyncio.sleep(4)
    async with container_install_requester as requester:
        # Add a user first
        util = get_utility(ILDAPUsers)

        assert 'Anna' == await util.exists('anna')
        assert await util.exists('anna3') is None

        await util.add_user('anna3')

        await util.add_user('anna2', 'Anna 2')

        assert 'Anna 2' == await util.exists('anna2')
        assert 'Anna 2' == await util.exists('anna2')
        assert await util.exists('anna3') is not None
