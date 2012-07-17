==========
privileges
==========

``privileges`` makes segmenting authenticated users easy and extensible.

Unlike Django permissions, ``privileges`` is not tied to operations on 
individual models. It operates at a higher level of abstraction and is instead
concerned more with providing the site developer complete freedom in determining
who can do what. There certainly is some overlap with the built in permissions
system, and while you could use ``privileges`` to replace it, at least large
parts of it, that is not the aim of this app.

Instead, think of ``privileges`` allowing the site developer to control
access to certain features. Operating at the template and view layers the site
developer can paint as broad or as fine of strokes to suit their needs.

It is extensible in the sense that the site developer can define and register
their own privilege validation handlers. In fact they must define at least one
handler. There is a template tag for checking privileges in templates and a
decorator for checking privileges when a view is called.

There is a model that stores the named privileges which are nothing more than
named slugs. The records carry no special meeting to ``privileges`` in isolation
but depend on the site developer to impart meaning through reference in his
site.


Sponsorship
-----------

development sponsored by `Midwest Communications`_


.. _`Midwest Communications`: http://mwcradio.com/