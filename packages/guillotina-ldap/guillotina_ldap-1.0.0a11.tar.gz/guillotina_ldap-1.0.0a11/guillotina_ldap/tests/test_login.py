import pytest
import json

@pytest.mark.asyncio
async def test_ldap_login(ldap, container_requester):
    async with container_requester as requester:
        resp, status_code = await requester(
            "POST",
            "/db/guillotina/@login",
            authenticated=False,
            data=json.dumps({"username": "anna", "password": "newsecret"}),
        )
        assert status_code == 200