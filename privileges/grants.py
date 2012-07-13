from django.contrib.auth.models import User

from privileges.models import Privilege


def privilege_list(grantor, grantee=None):
    return Privilege.objects.all()


def grantee_list(grantor, privilege=None):
    return User.objects.all().exclude(pk=grantor.pk)
