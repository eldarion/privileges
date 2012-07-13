from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME

from privileges import has_privilege


def privilege_required(privilege,
                       function=None,
                       redirect_field_name=None,
                       login_url=None):
    
    if redirect_field_name is None:
        redirect_field_name = REDIRECT_FIELD_NAME
    
    def test(user):
        if user.is_authenticated() and has_privilege(user, privilege):
            return True
        if user.is_superuser:
            return True
        return False
    
    actual_decorator = user_passes_test(
        test,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    
    if function:
        return actual_decorator(function)
    
    return actual_decorator
