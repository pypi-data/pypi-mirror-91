from warnings import warn

def depricateFunction(func, msg=""):
    """raise deprication warning on call
    
        raise depricated warning when func is called with msg "function {fun.name} is depricated"+msg"""
    def wrap(*args, **kwargs):
        warn(DeprecationWarning(f"{func.__name__} is depricated {msg}"))
        return func(*args, **kwargs)
    return wrap