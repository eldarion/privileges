__version__ = "0.1"


handlers = set()


def register(func):
    """
    func must have signature func(user, privilege) and return a boolean.
    """
    handlers.add(func)


def has_privilege(user, privilege):
    if user.is_anonymous():
        return False
    
    for handler in handlers:
        if handler(user, privilege):
            return True
    
    return False