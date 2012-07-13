from django.conf.urls.defaults import patterns, url


urlpatterns = patterns(
    "privileges.views",
    url(r"^(?P<username>\w+)/$", "grant_list",
        name="privileges_grant_list"
    ),
    url(r"^(?P<username>\w+)/(?P<pk>\d+)/$", "grant_detail",
        name="privileges_grant_detail"
    )
)
