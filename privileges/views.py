from django.http import HttpResponseForbidden, Http404
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext

from django.contrib.auth.models import User

from privileges.forms import GrantForm
from privileges.models import Grant


def list(request, username):
    
    user = get_object_or_404(User, username=username)
    if request.user != user and not request.user.is_superuser:
        return HttpResponseForbidden()
    
    if request.method == "POST":
        form = GrantForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            redirect("delegation_list", username=username)
    else:
        form = GrantForm(user=request.user)
    
    return render_to_response("delegation/list.html", {
        "grants_given": Grant.objects.filter(grantor=user),
        "grants_received": Grant.objects.filter(grantee=user),
        "grant_user": user,
        "form": form
    }, context_instance=RequestContext(request))


def detail(request, username, pk):
    
    user = get_object_or_404(User, username=username)
    if request.user != user and not request.user.is_superuser:
        return HttpResponseForbidden()
    
    grant = get_object_or_404(Grant, pk=pk)
    if grant.grantor != user and grant.grantee != user:
        return Http404()
    
    return render_to_response("delegation/detail.html", {
        "grant": grant,
        "grant_user": user
    }, context_instance=RequestContext(request))
