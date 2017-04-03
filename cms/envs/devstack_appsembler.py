# devstack_appsembler.py

from .devstack import *
from .appsembler import *

ENV_APPSEMBLER_FEATURES = ENV_TOKENS.get('APPSEMBLER_FEATURES', {})
for feature, value in ENV_APPSEMBLER_FEATURES.items():
    APPSEMBLER_FEATURES[feature] = value

INSTALLED_APPS += ('appsembler',)
DEFAULT_TEMPLATE_ENGINE['OPTIONS']['context_processors'] += ('appsembler.context_processors.intercom',)

CUSTOM_LOGOUT_REDIRECT_URL = ENV_TOKENS.get('CUSTOM_LOGOUT_REDIRECT_URL', '/')

TPA_CLEAN_USERNAMES_KEEP_DOMAIN_PART = ENV_TOKENS.get('TPA_CLEAN_USERNAMES_KEEP_DOMAIN_PART', False)
TPA_CLEAN_USERNAMES_REPLACER_CHAR = ENV_TOKENS.get('TPA_CLEAN_USERNAMES_REPLACER_CHAR', "")
TPA_CLEAN_USERNAMES_ADD_RANDOM_INT = ENV_TOKENS.get('TPA_CLEAN_USERNAMES_ADD_RANDOM_INT', False)

EDX_ORG_COURSE_API_URL = ENV_TOKENS.get('EDX_ORG_COURSE_API_URL', False)
EDX_ORG_COURSE_API_TOKEN_URL = AUTH_TOKENS.get('EDX_ORG_COURSE_API_TOKEN_URL', False)
EDX_ORG_COURSE_API_CLIENT_ID = AUTH_TOKENS.get('EDX_ORG_COURSE_API_CLIENT_ID', False)
EDX_ORG_COURSE_API_CLIENT_SECRET = AUTH_TOKENS.get('EDX_ORG_COURSE_API_CLIENT_SECRET', False)
EDX_ORG_COURSE_API_TOKEN_TYPE = AUTH_TOKENS.get('EDX_ORG_COURSE_API_TOKEN_TYPE', False)
EDX_ORG_COURSE_API_CATALOG_IDS = ENV_TOKENS.get('EDX_ORG_COURSE_API_CATALOG_IDS', False)

if APPSEMBLER_FEATURES.get('ENABLE_USAGE_TRACKING', False):
    INSTALLED_APPS += ('souvenirs',)
    MIDDLEWARE_CLASSES += ('souvenirs.middleware.SouvenirsMiddleware',)

    # appsembler devstack has dummy caches, but souvenirs needs a real cache
    # for rate-limiting writes to DB.
    SOUVENIRS_CACHE_NAME = 'souvenirs'
    CACHES[SOUVENIRS_CACHE_NAME] = {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'souvenirs',
    }
