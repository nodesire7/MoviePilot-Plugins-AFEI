from .main import run

PLUGIN_NAME = "HHSign"
PLUGIN_VERSION = "1.0.0"
PLUGIN_AUTHOR = "AFEI"
PLUGIN_DESCRIPTION = "HH论坛自动签到插件（Cookie版）"
plugin_icon = "signin.png"
author_url = "https://github.com/nodesire7/"

def load(user_provided_cookies=None):
    return lambda: run(user_provided_cookies)
