.. _installation:

Installation
============

* To install ::

    pip install privileges

* Add ``'privileges'`` to your ``INSTALLED_APPS`` setting::

    INSTALLED_APPS = (
        # other apps
        "privileges",
    )


After adding to your ``settings.INSTALLED_APPS``, you will need to add the
privileges you plan on using throughout your site. It is best to create them
using the ``/admin/`` and then as you make changes or add new ones, update your
``fixtures/initial_data.json`` fixture::

    ./manage.py dumpdata privileges --indent=4

Capture the output and merge it into your ``initial_data.json``.

