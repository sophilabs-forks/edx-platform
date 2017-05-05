# devstack_appsembler.py

from .devstack import *
from .appsembler import *

DEFAULT_TEMPLATE_ENGINE['OPTIONS']['context_processors'] += ('appsembler.context_processors.intercom',)

# disable caching in dev environment
for cache_key in CACHES.keys():
    CACHES[cache_key]['BACKEND'] = 'django.core.cache.backends.dummy.DummyCache'

SESSION_ENGINE = 'django.contrib.sessions.backends.db'

DISABLE_DJANGO_TOOLBAR = True
DISABLE_CONTRACTS = False

if DISABLE_DJANGO_TOOLBAR:
    from .common import INSTALLED_APPS, MIDDLEWARE_CLASSES

    def tuple_without(source_tuple, exclusion_list):
        """Return new tuple excluding any entries in the exclusion list. Needed because tuples
        are immutable. Order preserved."""
        return tuple([i for i in source_tuple if i not in exclusion_list])

    INSTALLED_APPS = tuple_without(INSTALLED_APPS, ['debug_toolbar', 'debug_toolbar_mongo'])
    MIDDLEWARE_CLASSES = tuple_without(MIDDLEWARE_CLASSES, [
        'django_comment_client.utils.QueryCountDebugMiddleware',
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ])

    DEBUG_TOOLBAR_MONGO_STACKTRACES = False

if DISABLE_CONTRACTS:
    import contracts
    contracts.disable_all()

INSTALLED_APPS += ('appsembler', 'study_location',)
