from privileges.registration import registry


class PrivilegesBackend(object):
    
    def has_perm(self, user_obj, perm, obj=None):
        if user_obj.is_anonymous():
            return False
        
        if registry.has_privilege(user_obj, perm):
            return True
        
        return super(PrivilegesBackend, self).has_perm(user_obj, perm)
