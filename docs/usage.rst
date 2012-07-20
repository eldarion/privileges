.. _usage:

Usage
=====

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

    from idios.models import ProfileBase
    from privileges.models import Privilege
    from privileges.registration import registry
    
    
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
    
    
    registry.register(has_privilege)


As you can see above, I added ``has_privilege`` and registered it with ``registry.register``.

The handler that you register can be any callable that takes two parameters, a
user object, and a string that matches the label of one of the privilege objects
in your database.


Achievement Based Privileges
****************************

Another example of how you might employ the use of ``privileges`` in your project
is by only giving users that have earned a certain reputation or score depending
on your chosen nomenclature. Using another open source app by Eldarion, ``brabeion``,
we can hook in the same type of handler.

First a quick setup of ``braebion``. Start an a new app in your project. Let's
call it ``glue`` as that's what it's doing -- gluing parts of different apps
together.  So in ``glue/badges.py`` you will have::

    from brabeion.base import Badge, BadgeAwarded
    
    
    class ProfileCompletionBadge(Badge):
        slug = "profile_completion"
        levels = [
            "Bronze",
            "Silver",
            "Gold",
        ]
        events = [
            "profile_updated",
        ]
        multiple = False
        
        def award(self, **state):
            user = state["user"]
            profile = user.get_profile()
            
            if profile.name and profile.about and profile.location and profile.website:
                return BadgeAwarded(level=3)
            elif profile.name and profile.about and profile.location:
                return BadgeAwarded(level=2)
            elif profile.name and profile.location:
                return BadgeAwarded(level=1)


Then in ``glue/models.py`` will want to create a model to link the ``ProfileCompletionBadge``
with a certain set of privileges. In addition, we write and register the
``has_privilege`` handler here as well::

    from django.db import models
    from django.db.models.signals import post_save
    
    from brabeion import badges
    
    from glue.badges import ProfileCompletionBadge
    from personas.models import DefaultPersona
    from privileges.models import Privilege
    from privileges.registration import registry
    
    
    BADGE_CHOICES = [
        (
            "%s:%s" % (ProfileCompletionBadge.slug, x[0]),
            "%s - %s" % (ProfileCompletionBadge.slug, x[1])
        )
        for x in enumerate(ProfileCompletionBadge.levels)
    ]
    
    
    class BadgePrivilege(models.Model):
    
        badge = models.CharField(max_length=128, choices=BADGE_CHOICES)
        privilege = models.ForeignKey(Privilege)
    
    
    def has_privilege(user, privilege):
        if not hasattr(user, "badges_earned"):
            return False
        
        for b in user.badges_earned.all():
            badge = "%s:%s" % (b.slug, b.level)
            if BadgePrivilege.objects.filter(
                badge=badge,
                privilege__label__iexact=privilege
            ).exists():
                return True
        
        return False
    
    
    def handle_saved_persona(sender, instance, created, **kwargs):
        badges.possibly_award_badge("profile_updated", user=instance.user)
    
    
    badges.register(ProfileCompletionBadge)
    post_save.connect(handle_saved_persona, sender=DefaultPersona)
    registry.register(has_privilege)


As you will notice from the code above, the implementation of the handler is
completely different from that of the Persona handler written about previously.
Don't be distracted by the braebion details around badges and whatnot, the
important thing to realize is that you, the site developer (or app developer),
can control exactly how different privileges are evaluated in contexts that
you control.

In addition, this example and the previous example where we attached privileges
to personas/profiles, are not mutually exclusive. They can work together. What
happens when privileges are checked is that all registered handlers are
evaluated until either it either finds one that evaluates to True or gets to the
end of all registered handlers, which it then will return False.

