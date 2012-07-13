import inspect


class Registry(object):
    
    def __init__(self):
        self.handlers = set()
    
    def register(self, func):
        """
        func must have signature func(user, privilege) and return a boolean.
        """
        assert callable(func)
        assert inspect.getargspec(func).args == ["user", "privilege"]
        self.handlers.add(func)
    
    def has_privilege(self, user, privilege):
        if user.is_anonymous():
            return False
        
        for handler in self.handlers:
            if handler(user=user, privilege=privilege):
                return True
        
        return False


registry = Registry()
