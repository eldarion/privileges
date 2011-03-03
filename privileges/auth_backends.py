from pinax.apps.account import auth_backends

import privileges


class AuthenticationBackend(auth_backends.AuthenticationBackend):
    supports_object_permissions = False
    supports_anonymous_user = True
    
    def has_perm(self, user, perm):
        if user.is_anonymous():
            return False
        
        if privileges.has_privilege(user, perm):
            return True
        
        return super(AuthenticationBackend, self).has_perm(user, perm)