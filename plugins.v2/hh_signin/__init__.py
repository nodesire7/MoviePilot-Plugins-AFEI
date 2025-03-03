from .main import run

def load(user_provided_cookies=None):
    return lambda: run(user_provided_cookies)
