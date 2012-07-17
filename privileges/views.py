import urlparse

from functools import wraps

from django.db.models import Q
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.decorators import available_attrs, method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

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


class UsernameContextMixin(object):
    
    def get_context_data(self, **kwargs):
        context = super(UsernameContextMixin, self).get_context_data(**kwargs)
        context.update({
            "username": self.kwargs.get("username")
        })
        return context


@cbv_decorator(owner_required)
class GrantListView(UsernameContextMixin, ListView):
    model = Grant
    
    def get_queryset(self):
        username = self.kwargs["username"]
        return super(GrantListView, self).get_queryset().filter(
            Q(grantor__username=username) | Q(grantee__username=username)
        )


@cbv_decorator(owner_required)
class GrantCreateView(UsernameContextMixin, CreateView):
    model = Grant
    form_class = GrantForm
    
    def get_form_kwargs(self):
        kwargs = super(GrantCreateView, self).get_form_kwargs()
        kwargs.update({
            "user": self.request.user
        })
        return kwargs
    
    def get_success_url(self):
        return reverse(
            "privileges_grant_list",
            kwargs={"username": self.request.user.username}
        )


@cbv_decorator(owner_required)
class GrantUpdateView(UsernameContextMixin, UpdateView):
    model = Grant
    form_class = GrantForm
    
    def get_form_kwargs(self):
        kwargs = super(GrantUpdateView, self).get_form_kwargs()
        kwargs.update({
            "user": self.request.user
        })
        return kwargs
    
    def get_success_url(self):
        return reverse(
            "privileges_grant_list",
            kwargs={"username": self.request.user.username}
        )


@cbv_decorator(owner_required)
class GrantDeleteView(UsernameContextMixin, DeleteView):
    model = Grant
    
    def get_success_url(self):
        return reverse(
            "privileges_grant_list",
            kwargs={"username": self.request.user.username}
        )


