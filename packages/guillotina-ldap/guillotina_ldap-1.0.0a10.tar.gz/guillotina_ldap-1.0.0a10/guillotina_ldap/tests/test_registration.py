from guillotina.component import get_utility
from guillotina.interfaces import IMailer
import pytest
import json
import asyncio

user_data = {
    "id": "foobar",
    "password": "password",
    "fullname": "Foobar 2"
}

user_data2 = {
    "id": "foobar",
    "fullname": "User Foo",
}


@pytest.mark.parametrize("install_addons", [["email_validation"]])
@pytest.mark.asyncio
async def test_ldap_auth(ldap, container_install_requester):
    await asyncio.sleep(4)
    async with container_install_requester as requester:
        # Add a user first
        resp, status_code = await requester(
            "POST", "/db/guillotina/@users", authenticated=False, data=json.dumps(user_data)
        )
        assert status_code == 200

        util = get_utility(IMailer)
        assert "http://localhost:4200/@@validation" in util.mail[0]["html"]
        assert "Registering user Foobar 2" in util.mail[0]["html"]

        token = (
            util.mail[0]["html"]
            .split("http://localhost:4200/@@validation?token=")[1]
            .split('" target="_blank"')[0]
        )

        resp, status_code = await requester(
            "POST", f"/db/guillotina/@validate/{token}", data=json.dumps({}), authenticated=False
        )
        assert "token" in resp
        assert status_code == 200

        resp, status_code = await requester(
            "POST",
            "/db/guillotina/@login",
            authenticated=False,
            data=json.dumps({"username": "foobar", "password": "password"}),
        )
        assert status_code == 200

        resp, status_code = await requester(
            "POST", "/db/guillotina/@users", authenticated=False, data=json.dumps(user_data)
        )
        assert status_code == 200


@pytest.mark.parametrize("install_addons", [["email_validation"]])
@pytest.mark.asyncio
async def test_ldap_auth_2nd(ldap, container_install_requester):
    await asyncio.sleep(4)
    async with container_install_requester as requester:
        # Add a user first
        resp, status_code = await requester(
            "POST", "/db/guillotina/@users", authenticated=False, data=json.dumps(user_data2)
        )
        assert status_code == 200

        util = get_utility(IMailer)
        assert "http://localhost:4200/@@validation" in util.mail[0]["html"]
        assert "<p>Registering user User Foo</p>" in util.mail[0]["html"]

        token = (
            util.mail[0]["html"]
            .split("http://localhost:4200/@@validation?token=")[1]
            .split('" target="_blank"')[0]
        )

        resp, status_code = await requester(
            "POST", f"/db/guillotina/@validate/{token}", data=json.dumps({"password": "password"}), authenticated=False
        )
        assert "token" in resp
        assert status_code == 200

        resp, status_code = await requester(
            "POST",
            "/db/guillotina/@login",
            authenticated=False,
            data=json.dumps({"username": "foobar", "password": "password"}),
        )
        assert status_code == 200

        resp, status_code = await requester(
            "POST", "/db/guillotina/@users", authenticated=False, data=json.dumps(user_data)
        )
        assert status_code == 200