from django.conf.urls.defaults import patterns, url

from privileges import views


urlpatterns = patterns(
    "",
    url(r"^(?P<username>\w+)/$",
        views.GrantListView.as_view(),
        name="privileges_grant_list"
    ),
    url(r"^(?P<username>\w+)/create/$",
        views.GrantCreateView.as_view(),
        name="privileges_grant_create"
    ),
    url(r"^(?P<username>\w+)/(?P<pk>\d+)/update/$",
        views.GrantUpdateView.as_view(),
        name="privileges_grant_update"
    ),
    url(r"^(?P<username>\w+)/(?P<pk>\d+)/delete/$",
        views.GrantDeleteView.as_view(),
        name="privileges_grant_delete"
    )
)
