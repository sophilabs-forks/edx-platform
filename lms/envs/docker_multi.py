from .docker import *

# Override the default Elasticsearch configuration for edx-search
ELASTIC_SEARCH_CONFIG = ['elasticsearch:9200']

# Needed to enable course discovery
SEARCH_SKIP_ENROLLMENT_START_DATE_FILTERING = True
