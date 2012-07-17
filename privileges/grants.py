import sys

from django.conf import settings
from django.contrib.auth.models import User

from privileges.models import Privilege


def import_obj(name):
    dot = name.rindex('.')
    mod_name, obj_name = name[:dot], name[dot+1:]
    __import__(mod_name)
    return getattr(sys.modules[mod_name], obj_name)


def _privilege_list(grantor, grantee=None):
    return Privilege.objects.all()


def _grantee_list(grantor, privilege=None):
    return User.objects.all().exclude(pk=grantor.pk)


privilege_list = import_obj(
    getattr(settings, "PRIVILEGES_PRIVILEGE_LIST_CALLABLE", "privileges.grants._privilege_list")
)

grantee_list = import_obj(
    getattr(settings, "PRIVILEGES_GRANTEE_LIST_CALLABLE", "privileges.grants._grantee_list")
)