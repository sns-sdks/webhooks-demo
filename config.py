"""
    Config
"""

FACEBOOK_VERIFY_TOKEN = "facebook"

try:
    from local_settings import *  # noqa
except ImportError:
    pass
