from django.conf.urls.defaults import patterns, url


urlpatterns = patterns(
    "delegation.views",
    url(r"^(?P<username>\w+)/$", "list",
        name="delegation_list"
    ),
    url(r"^(?P<username>\w+)/(?P<pk>\d+)/$", "detail",
        name="delegation_detail"
    )
)
