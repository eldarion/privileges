.. _decorators:


Decorators
==========

While the template tag is good to control bits in the UI, you will likely want
to make sure POST requests can't be forged. Just because you don't show a form
in the UI, doesn't mean there isn't a url accepting POST requests. This is the
reason for the ``privilege_required`` decorator.

By putting this decorator on views, it will validate that the user calling the
view as the specified privilege, otherwise it will redirect, by default, to
the login url::

    from privileges.decorators import privilege_required
    
    
    @privilege_required("widget_management_feature_enabled")
    def add_widget(request):
        ....
