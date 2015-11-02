from .docker import *

# Override the default Elasticsearch configuration for edx-search
ELASTIC_SEARCH_CONFIG = ['elasticsearch:9200']

# Settings for S3 static assets
AWS_IS_GZIPPED = True
AWS_HEADERS = {'Cache-Control': 'public, max-age=86400'}
