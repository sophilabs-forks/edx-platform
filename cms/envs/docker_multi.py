from .docker import *

CACHES = {
    "celery": {
        "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
        "KEY_FUNCTION": "util.memcache.safe_key",
        "KEY_PREFIX": "celery",
        "LOCATION": [
            "{}:{}".format(os.environ.get("CACHE_DNS_HOST", "memcached"), os.environ.get("CACHE_DNS_PORT", 11211))
        ],
        "TIMEOUT": "7200"
    },
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
        "KEY_FUNCTION": "util.memcache.safe_key",
        "KEY_PREFIX": "default",
        "LOCATION": [
            "{}:{}".format(os.environ.get("CACHE_DNS_HOST", "memcached"), os.environ.get("CACHE_DNS_PORT", 11211))
        ]
    },
    "general": {
        "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
        "KEY_FUNCTION": "util.memcache.safe_key",
        "KEY_PREFIX": "general",
        "LOCATION": [
            "{}:{}".format(os.environ.get("CACHE_DNS_HOST", "memcached"), os.environ.get("CACHE_DNS_PORT", 11211))
        ]
    },
    "mongo_metadata_inheritance": {
        "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
        "KEY_FUNCTION": "util.memcache.safe_key",
        "KEY_PREFIX": "mongo_metadata_inheritance",
        "LOCATION": [
            "{}:{}".format(os.environ.get("CACHE_DNS_HOST", "memcached"), os.environ.get("CACHE_DNS_PORT", 11211))
        ],
        "TIMEOUT": 300
    },
    "staticfiles": {
        "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
        "KEY_FUNCTION": "util.memcache.safe_key",
        "KEY_PREFIX": "9818fcbe520e_general",
        "LOCATION": [
            "{}:{}".format(os.environ.get("CACHE_DNS_HOST", "memcached"), os.environ.get("CACHE_DNS_PORT", 11211))
        ]
    }
}

CONTENTSTORE = {
    "ADDITIONAL_OPTIONS": {},
    "DOC_STORE_CONFIG": {
        "collection": "modulestore",
        "db": "docker-edxapp",
        "host": [
            os.environ.get("MONGO_DNS_HOST", "mongo")
        ],
        "password": "daheiYae2c",
        "port": int(os.environ.get("MONGO_DNS_PORT", 27017)),
        "user": "edxapp"
    },
    "ENGINE": "xmodule.contentstore.mongo.MongoContentStore",
    "OPTIONS": {
        "db": "docker-edxapp",
        "host": [
            os.environ.get("MONGO_DNS_HOST", "mongo")
        ],
        "password": "daheiYae2c",
        "port": int(os.environ.get("MONGO_DNS_PORT", 27017)),
        "user": "edxapp"
    }
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "HOST": os.environ.get("DB_DNS_HOST", "db"),
        "NAME": "edxapp",
        "PASSWORD": "password",
        "PORT": os.environ.get("DB_DNS_PORT", 3306),
        "USER": "edxapp001"
    },
    "read_replica": {
        "ENGINE": "django.db.backends.mysql",
        "HOST": os.environ.get("DB_DNS_HOST", "db"),
        "NAME": "edxapp",
        "PASSWORD": "password",
        "PORT": os.environ.get("DB_DNS_PORT", 3306),
        "USER": "edxapp001"
    }
}

DOC_STORE_CONFIG = {
    "collection": "modulestore",
    "db": "docker-edxapp",
    "host": [
        os.environ.get("MONGO_DNS_HOST", "mongo")
    ],
    "password": "daheiYae2c",
    "port": int(os.environ.get("MONGO_DNS_PORT", 27017)),
    "user": "edxapp"
}

MODULESTORE = {
    "default": {
        "ENGINE": "xmodule.modulestore.mixed.MixedModuleStore",
        "OPTIONS": {
            "mappings": {},
            "stores": [
                {
                    "DOC_STORE_CONFIG": {
                        "collection": "modulestore",
                        "db": "edxapp",
                        "host": [
                            os.environ.get("MONGO_DNS_HOST", "mongo")
                        ],
                        "password": "password",
                        "port": int(os.environ.get("MONGO_DNS_PORT", 27017)),
                        "user": "edxapp"
                    },
                    "ENGINE": "xmodule.modulestore.mongo.DraftMongoModuleStore",
                    "NAME": "draft",
                    "OPTIONS": {
                        "default_class": "xmodule.hidden_module.HiddenDescriptor",
                        "fs_root": "/edx/var/edxapp/data",
                        "render_template": "edxmako.shortcuts.render_to_string"
                    }
                },
                {
                    "ENGINE": "xmodule.modulestore.xml.XMLModuleStore",
                    "NAME": "xml",
                    "OPTIONS": {
                        "data_dir": "/edx/var/edxapp/data",
                        "default_class": "xmodule.hidden_module.HiddenDescriptor"
                    }
                },
                {
                    "DOC_STORE_CONFIG": {
                        "collection": "modulestore",
                        "db": "edxapp",
                        "host": [
                            os.environ.get("MONGO_DNS_HOST", "mongo")
                        ],
                        "password": "password",
                        "port": int(os.environ.get("MONGO_DNS_PORT", 27017)),
                        "user": "edxapp"
                    },
                    "ENGINE": "xmodule.modulestore.split_mongo.split_draft.DraftVersioningModuleStore",
                    "NAME": "split",
                    "OPTIONS": {
                        "default_class": "xmodule.hidden_module.HiddenDescriptor",
                        "fs_root": "/edx/var/edxapp/data",
                        "render_template": "edxmako.shortcuts.render_to_string"
                    }
                }
            ]
        }
    }
}

# Override the default Elasticsearch configuration for edx-search
ELASTIC_SEARCH_CONFIG = ['elasticsearch:9200']
