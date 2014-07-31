.. _templatetags:


Template Tags
=============

In order to assist in validating privileges in the template to control bits of
your UI, there is a template tag called ``check_privilege`` and it is used like
so::

    {% load privileges_tags %}
    ....
    {% check_privilege 'foo_feature_enabled' for user as has_foo %}

    {% if has_foo %}
        ....
    {% endif %}
