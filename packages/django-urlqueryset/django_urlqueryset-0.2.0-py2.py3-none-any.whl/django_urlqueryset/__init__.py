from .urlqueryset import *

VERSION = (0, 2, 0)

__version__ = '.'.join([str(n) for n in VERSION])


def get_version():
    return __version__


default_app_config = 'django_urlqueryset.apps.CheckConfig'

