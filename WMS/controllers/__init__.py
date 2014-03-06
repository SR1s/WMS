import functools

def verify_login(func):
    @functools.wraps(func)
    def wrappper():
        # test if login
        func()
        # do something else
    return wrappper