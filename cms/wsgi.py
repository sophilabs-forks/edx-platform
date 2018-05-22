# Patch the xml libs before anything else.
# Bryan: don't do this for now, while testing Diazo
# FIXME: figure out a way to not 'defuse' in context of Diazo middleware
# from safe_lxml import defuse_xml_libs
# defuse_xml_libs()

# Disable PyContract contract checking when running as a webserver
import contracts
contracts.disable_all()

import openedx.core.operations
openedx.core.operations.install_memory_dumper()

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cms.envs.aws")

import cms.startup as startup
startup.run()

# This application object is used by the development server
# as well as any WSGI server configured to use this file.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django_diazo.wsgi import DiazoMiddlewareWrapper
application = DiazoMiddlewareWrapper(application)
