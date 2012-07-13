from django import template

import privileges


register = template.Library()


class CheckPrivilegeNode(template.Node):
    
    @classmethod
    def handle_token(cls, parser, token):
        bits = token.split_contents()
        if len(bits) != 6:
            raise template.TemplateSyntaxError
        if bits[2] != "for" and bits[4] != "as":
            raise template.TemplateSyntaxError
        return cls(
            parser.compile_filter(bits[1]),
            parser.compile_filter(bits[3]),
            bits[5]
        )
    
    def __init__(self, privilege, user, varname):
        self.privilege = privilege
        self.user = user
        self.varname = varname
    
    def render(self, context):
        privilege = self.privilege.resolve(context)
        user = self.user.resolve(context)
        context[self.varname] = privileges.has_privilege(user, privilege)
        return ""


@register.tag
def check_privilege(parser, token):
    """
    Usage::
        {% check_privilege 'privilege' for user as has_privilege %}
    """
    return CheckPrivilegeNode.handle_token(parser, token)
