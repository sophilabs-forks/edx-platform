"""Utility functions and classes for track backends"""

import json
from datetime import datetime, date

from pytz import UTC

from openedx.core.djangoapps.site_configuration.models import SiteConfiguration


class DateTimeJSONEncoder(json.JSONEncoder):
    """JSON encoder aware of datetime.datetime and datetime.date objects"""

    def default(self, obj):  # pylint: disable=method-hidden
        """
        Serialize datetime and date objects of iso format.

        datatime objects are converted to UTC.
        """

        if isinstance(obj, datetime):
            if obj.tzinfo is None:
                # Localize to UTC naive datetime objects
                obj = UTC.localize(obj)
            else:
                # Convert to UTC datetime objects from other timezones
                obj = obj.astimezone(UTC)
            return obj.isoformat()
        elif isinstance(obj, date):
            return obj.isoformat()

        return super(DateTimeJSONEncoder, self).default(obj)


def get_site_configuration_from_request(request):
    try:
        site_configuration = request.site.configuration.values
    except:
        site_configuration = None
    return site_configuration


def get_site_configuration(site_id):
    try:
        site_configuration = SiteConfiguration.objects.get(pk=site_id).values
    except SiteConfiguration.DoesNotExist:
        site_configuration = None
    return site_configuration
