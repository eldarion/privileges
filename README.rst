==========
privileges
==========

``privileges`` is an extensible Django app that provides ....


Overview
--------

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


Getting Started
---------------

Installation::

    pip install privileges


Configuration (settings.py)::

    INSTALLED_APPS = [
        ....
        "privileges",
        ....
    ]

After adding to your ``settings.INSTALLED_APPS``, you will need to add the
privileges you plan on using throughout your site. It is best to create them
using the ``/admin/`` and then as you make changes or add new ones, update your
``fixtures/initial_data.json`` fixture::

    ./manage.py dumpdata privileges --indent=4

Capture the output and merge it into your ``initial_data.json``.


Examples
--------

The best way to familiarize yourself with ``privileges`` is to walk through
some examples. So let's get started.


Profile Based Privileges
************************

You are building a site that has a number of different personas so you decide to
model that using ``idios`` and end up with something that looks like::

    from idios.models import ProfileBase
    
    
    class Persona(ProfileBase):
    
        name = models.CharField(max_length=50, null=True, blank=True)
    
    
    class MemberPersona(Persona):
    
        expired = models.BooleanField(default=False)
    
    
    class StaffPersona(Persona):
    
        pass


You will need to add and register a privileges handler::

    import privileges
    
    from idios.models import ProfileBase
    from privileges.models import Privilege
    
    
    class Persona(ProfileBase):
    
        name = models.CharField(max_length=50, null=True, blank=True)
    
    
    class MemberPersona(Persona):
    
        expired = models.BooleanField(default=False)
    
    
    class StaffPersona(Persona):
    
        pass
    
    
    class PersonaPrivilege(models.Model):
        
        persona_type = models.ForeignKey(ContentType)
        privilege = models.ForeignKey(Privilege)
        
        class Meta:
            verbose_name = "Persona Privilege"
            unique_together = ["persona_type", "privilege"]
        
        def __unicode__(self):
            return unicode("%s has '%s'" % (self.persona_type, self.privilege.label))
    
    
    def has_privilege(user, privilege):
        """
        Checks each Persona that a user has and it's privileges
        """
        if user.is_superuser:
            return True
        
        for p in [MemberPersona, StaffPersona]:
            for persona in p.objects.filter(user=user):
                ct_type = ContentType.objects.get_for_model(persona)
                if PersonaPrivilege.objects.filter(
                    persona_type=ct_type,
                    privilege__label=privilege
                ).exists():
                    return True
        return False
    
    
    privileges.register(has_privilege)


Delegated Privileges
********************


Achievement Based Privileges
****************************


Privileges in the Template
**************************


Privileges in the View
**********************

