from pytest_docker_fixtures.containers._base import BaseImage
from pytest_docker_fixtures.images import settings
from guillotina import testing
import pytest
from bonsai import LDAPClient, LDAPEntry, LDAPModOp

def base_settings_configurator(settings):
    if 'applications' in settings:
        settings['applications'].append('guillotina_ldap')
        settings['applications'].append('guillotina.contrib.mailer')
        settings['applications'].append('guillotina.contrib.email_validation')
    else:
        settings['applications'] = ['guillotina.contrib.mailer', 'guillotina.contrib.email_validation', 'guillotina_ldap']
    settings["mailer"] = {
      "default_sender": "foo@bar.com",
      "endpoints": {
        "default": {
          "type": "smtp",
          "host": "localhost",
          "port": 25
        }
      },
      "utility": "guillotina.contrib.mailer.utility.TestMailerUtility"
    }

    settings["auth_token_validators"] = [
        "guillotina.auth.validators.SaltedHashPasswordValidator",
        "guillotina.auth.validators.JWTValidator",
        "guillotina_ldap.validator.LDAPPasswordValidator"
    ]
    settings["auth_user_identifiers"] = [
        "guillotina_ldap.user.LDAPUserIdentifier"
    ]

    settings["ldap"] = {
        "managerdn": "cn=admin,dc=my-company,dc=com",
        "managerpwd": "secret",
        "usersdn": "dc=my-company,dc=com",
        "managers": ["bob"],
        "objecttype": "inetOrgPerson",
        "attribute_users": "uid",
        "host": f"ldap://{LDAPCONFIG['host']}:{LDAPCONFIG['port']}"
    }
    settings["allow_register"] = True,
    settings["_fake_recaptcha_"] = "FAKE_RECAPTCHA",


testing.configure_with(base_settings_configurator)

settings['ldap'] = {
    'max_wait_s': 30,
    'image': 'osixia/openldap',
    'version': '1.4.0',
    'env': {
        'LDAP_ORGANISATION': 'My Company',
        'LDAP_DOMAIN': 'my-company.com',
        'LDAP_ADMIN_PASSWORD': 'secret'
    },
    'options': {
        'mem_limit': '200m',
    }
}

LDAPCONFIG = {
    "host": None,
    "port": None
}

class LDAP(BaseImage):
    name = 'ldap'
    port = 389

    def check(self):
        import bonsai

        conn = None
        cur = None
        try:
            client = bonsai.LDAPClient(f"ldap://{self.host}:{self.get_port()}")

            try:
                con = client.connect()
            finally:
                pass
            return True
        except Exception:
            return False


ldap_image = LDAP()

@pytest.fixture(scope='session')
def ldap():
    result = ldap_image.run()
    LDAPCONFIG['host'] = result[0]
    LDAPCONFIG['port'] = result[1]
    client = LDAPClient(f"ldap://{LDAPCONFIG['host']}:{LDAPCONFIG['port']}")
    client.set_credentials("SIMPLE", user='cn=admin,dc=my-company,dc=com', password='secret')
    conn = client.connect()

    anna = LDAPEntry("uid=anna,dc=my-company,dc=com")
    anna['objectClass'] = ['top', 'inetOrgPerson']
    anna['sn'] = "Wu"
    anna['cn'] = "Wu"
    anna['uid'] = "anna"
    anna['displayName'] = "Anna"
    conn.add(anna)
    anna.change_attribute("userPassword", LDAPModOp.REPLACE, "newsecret")
    anna.modify()
    yield result
    ldap_image.stop()
