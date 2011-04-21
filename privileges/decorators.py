from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME

from privileges import has_privilege


def privilege_required(privilege, function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user has the right privileges,
    redirecting to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: (u.is_authenticated() and has_privilege(u, privilege)) or u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
