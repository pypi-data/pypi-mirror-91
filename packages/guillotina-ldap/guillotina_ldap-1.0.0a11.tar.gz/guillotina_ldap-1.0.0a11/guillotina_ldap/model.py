from guillotina.auth.users import GuillotinaUser
from guillotina.component import get_utility
from guillotina_ldap.interfaces import ILDAPUsers


class LDAPGuillotinaUser(GuillotinaUser):

    async def set_password(self, password, oldpassword=None):
        util = get_utility(ILDAPUsers)
        set_password = False
        if oldpassword is not None and await util.validate_user(self.id, oldpassword):
            set_password = True
        elif oldpassword is None:
            set_password = True

        if set_password:
            await util.set_password(self.id, password)
