from .aws import *

INSTALLED_APPS += ('appsembler_cms', 'appsembler_lms',)
APPSEMBLER_AMC_API_BASE = AUTH_TOKENS.get('APPSEMBLER_AMC_API_BASE')
APPSEMBLER_FIRST_LOGIN_API = '/logged_into_edx'

APPSEMBLER_SECRET_KEY = AUTH_TOKENS.get("APPSEMBLER_SECRET_KEY")

EMAIL_BACKEND = 'django_mailgun.MailgunBackend'
MAILGUN_ACCESS_KEY = AUTH_TOKENS.get("MAILGUN_ACCESS_KEY")
MAILGUN_SERVER_NAME = AUTH_TOKENS.get("MAILGUN_SERVER_NAME")


# SENTRY
SENTRY_DSN = AUTH_TOKENS.get('SENTRY_DSN', False)

if SENTRY_DSN:
    # Set your DSN value
    RAVEN_CONFIG = {
        'dsn': SENTRY_DSN,
    }

    INSTALLED_APPS += ('raven.contrib.django.raven_compat',)

# CMS needs MEDIA_ settings for SCORM XBlock
MEDIA_ROOT = '/edx/var/edxapp/media'
MEDIA_URL = '/media/'
