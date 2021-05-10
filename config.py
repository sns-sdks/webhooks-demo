"""
    Config
"""

# Facebook
FACEBOOK_VERIFY_TOKEN = "facebook"

# Twitter
TWITTER_CONSUMER_KEY = "your app consumer key"
TWITTER_CONSUMER_SECRET = "your app consumer secret"
TWITTER_ACCESS_TOKEN = "your app access token"
TWITTER_ACCESS_SECRET = "your app access secret"

# secret
SECURITY_CHECK = False

try:
    from local_settings import *  # noqa
except ImportError:
    pass
