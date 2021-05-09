"""
    Config
"""

# Facebook
FACEBOOK_VERIFY_TOKEN = "facebook"

# Twitter
TWITTER_CONSUMER_SECRET = "your app consumer secret"

# secret
SECURITY_CHECK = False

try:
    from local_settings import *  # noqa
except ImportError:
    pass
