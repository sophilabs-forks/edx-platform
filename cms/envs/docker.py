import os
from .aws_appsembler import *

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.mandrillapp.com"
EMAIL_PORT = 2525
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "nate@appsembler.com"
EMAIL_HOST_PASSWORD = (APPSEMBLER_FEATURES.get("MANDRILL_API_KEY","") or os.environ.get("MANDRILL_API_KEY", ""))

LMS_BASE = (ENV_TOKENS.get("LMS_BASE","") or os.environ.get("EDX_LMS_BASE", ""))
CMS_BASE = (ENV_TOKENS.get("CMS_BASE","") or os.environ.get("EDX_CMS_BASE", ""))
FEATURES.update(PREVIEW_LMS_BASE=(ENV_FEATURES.get("PREVIEW_LMS_BASE","") or os.environ.get("EDX_PREVIEW_LMS_BASE", "")))

SITE_NAME = LMS_BASE

default_email = ENV_TOKENS.get("DEFAULT_FROM_EMAIL","")
DEFAULT_FROM_EMAIL = 'registration@appsembler.com' if default_email == "registration@example.com" else default_email

#can probably be clean up later
env_platform_name = ENV_TOKENS.get("PLATFORM_NAME","")
PLATFORM_NAME = 'Appsembler Open edX Testdrive' if env_platform_name == "Your Platform Name Here" else env_platform_name

# Needed for the recommender XBlock
ALLOW_ALL_ADVANCED_COMPONENTS = True
