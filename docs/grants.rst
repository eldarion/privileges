.. _grants:


Grants
======

Privileges can be granted to other users and who is allowed to grant what to
whom can be controlled via the implementation of a couple site level
callables. It defaults to a wide-open system. In other words, no restrictions
on anyone granting any of their privileges to any other user in the site.

Grants are an entirely optional feature. Simply don't add the urls and the
feature will be inaccessible to users.


Installation
------------

To add grants to your site, you are essnetially just exposing the UI to your
users to be able to create and manage their grants. The simplest form of
enabling granting is::

    ...
    url(r"^privileges/", include("privileges.urls")),
    ...

This will add four urls to your url configuration:

* ``privileges_grant_list``
* ``privileges_grant_create``
* ``privileges_grant_update``
* ``privileges_grant_delete``

These all take ``username`` as a kwarg and the update and delete urls also take
the ``pk`` of the grant objecct. You might want to link to this pages under an
account settings interface for the user in your site somewhere.


privileges_grant_list
^^^^^^^^^^^^^^^^^^^^^

:kwargs: username
:context: grants_list, username
:template: ``privileges/grant_list.html``

This view will display the user's grants and the requesting user has to
either match the usenrame or be a superuser. It will render a template
stored at ``privileges/grant_list.html`` and a default template that
exiends ``site_base.html`` has been included in this package.


privileges_grant_create
^^^^^^^^^^^^^^^^^^^^^^^

:kwargs: username
:context: form, username
:template: ``privileges/grant_form.html``

This view handles the form display and POST handling to create new grants.


privileges_grant_update
^^^^^^^^^^^^^^^^^^^^^^^

:kwargs: username, pk
:context: form, grant, username
:template: ``privileges/grant_form.html``

This view handles the form display and POST handling to update existing grants.


privileges_grant_delete
^^^^^^^^^^^^^^^^^^^^^^^

:kwargs: username, pk
:context: form, grant, username
:template: ``privileges/grant_confirm_delete.html``

This view handles the form display and POST handling to delete grants.


Customization
-------------

There are two callables that you can define in your site and configure
via settings. They currently default to::

    PRIVILEGES_PRIVILEGE_LIST_CALLABLE = "privileges.grants._privilege_list"
    PRIVILEGES_GRANTEE_LIST_CALLABLE = "privileges.grants._grantee_list"

These should be callables that are importable within the context of your
site. Futhermore, they are expected to have the following argspecs::

    privilege_list(grantor, grantee=None)
    
    grantee_list(grantor, privilege=None)

Where ``grantor`` and ``grantee`` are ``auth.User`` objects, and ``privilege``
is a ``privileges.Privilege`` object.

These functions are what control the options in the
``privileges.forms.GrantForm`` that validate and allow the creation of new
grants by users of your site.

These functions currently return all privileges and all users (excluding
only the ``grantor`` from the list), so it is wide open by default, and is
up to you to implement the business rules for how these lists should be
constrained.

