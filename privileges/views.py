import urlparse

from functools import wraps

from django.conf import settings
from django.utils.decorators import available_attrs, method_decorator

from django.contrib.auth import REDIRECT_FIELD_NAME

from privileges.forms import GrantForm
from privileges.models import Grant


def owner_required(view_func):
    @wraps(view_func, assigned=available_attrs(view_func))
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated():
            if request.user.username == kwargs["username"] or \
               request.user.is_superuser:
                return view_func(request, *args, **kwargs)
        path = request.build_absolute_uri()
        login_scheme, login_netloc = urlparse.urlparse(settings.LOGIN_URL)[:2]
        current_scheme, current_netloc = urlparse.urlparse(path)[:2]
        if ((not login_scheme or login_scheme == current_scheme) and
            (not login_netloc or login_netloc == current_netloc)):
            path = request.get_full_path()
        from django.contrib.auth.views import redirect_to_login
        return redirect_to_login(path, redirect_field_name=REDIRECT_FIELD_NAME)
    return _wrapped_view


def cbv_decorator(decorator):
    def _decorator(cls):
        cls.dispatch = method_decorator(decorator)(cls.dispatch)
        return cls
    return _decorator


    
    
    


    
    
    
