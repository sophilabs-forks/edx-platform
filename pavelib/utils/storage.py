import os
import posixpath
from urllib import unquote

from django.contrib.staticfiles.storage import CachedFilesMixin, \
    StaticFilesStorage
from pipeline.storage import PipelineMixin
from storages.backends.s3boto import S3BotoStorage


from django.contrib.staticfiles.storage import CachedFilesMixin


class ASCachedFilesMixin(CachedFilesMixin):
    """A Cached files mixin that handles slashes properly, so that we can use
    Pipeline with ``url(//fonts.google.com//*)``.
    """

    # WORKAROUND: URLs that start with // should also be matched, so we're
    # overriding this method to patch it. See
    # https://github.com/cyberdelia/django-pipeline/issues/179. This issue is
    # fixed as of Django 1.5, so this workaround should be removed after
    # upgrading.
    def url_converter(self, name):
        """
        Returns the custom URL converter for the given file name.
        """
        def converter(matchobj):
            """
            Converts the matched URL depending on the parent level (`..`)
            and returns the normalized and hashed URL using the url method
            of the storage.
            """
            matched, url = matchobj.groups()
            # Completely ignore http(s) prefixed URLs,
            # fragments and data-uri URLs

            # This line is the only thing we changed.
            # See: https://github.com/django/django/blob/stable/1.4.x/django/contrib/staticfiles/storage.py#L147
            if url.startswith(('#', 'http:', 'https:', 'data:', '//')):
                return matched
            name_parts = name.split(os.sep)
            # Using posix normpath here to remove duplicates
            url = posixpath.normpath(url)
            url_parts = url.split('/')
            parent_level, sub_level = url.count('..'), url.count('/')
            if url.startswith('/'):
                sub_level -= 1
                url_parts = url_parts[1:]
            if parent_level or not url.startswith('/'):
                start, end = parent_level + 1, parent_level
            else:
                if sub_level:
                    if sub_level == 1:
                        parent_level -= 1
                    start, end = parent_level, 1
                else:
                    start, end = 1, sub_level - 1
            joined_result = '/'.join(name_parts[:-start] + url_parts[end:])
            hashed_url = self.url(unquote(joined_result), force=True)
            file_name = hashed_url.split('/')[-1:]
            relative_url = '/'.join(url.split('/')[:-1] + file_name)

            # Return the hashed version to the file
            return 'url("%s")' % unquote(relative_url)
        return converter


class S3PrefixedStorage(S3BotoStorage):
    """A storage backend that allows the addition of a prefix for files stored
    via S3BotoStorage.
    """

    def __init__(self, *args, **kwargs):
        from django.conf import settings
        if hasattr(settings, 'AWS_STORAGE_BUCKET_PREFIX'):
            kwargs['location'] = settings.AWS_STORAGE_BUCKET_PREFIX
        return super(S3PrefixedStorage, self).__init__(*args, **kwargs)


class S3ZippedPipelineStorage(PipelineMixin, ASCachedFilesMixin, S3PrefixedStorage):
    pass
