# aws_appsembler.py

from .aws import *
from .appsembler import *

INSTALLED_APPS += ('appsembler','aquent_data_migration','accredible_certificate',)

TEMPLATE_CONTEXT_PROCESSORS += ('appsembler.context_processors.intercom',)
