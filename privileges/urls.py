from django.conf.urls.defaults import patterns, url

from privileges import views


urlpatterns = patterns(
    "",
    url(r"^(?P<username>\w+)/$",
        views.GrantListView.as_view(),
        name="privileges_grant_list"
    ),
    )
)
