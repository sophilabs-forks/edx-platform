from __future__ import absolute_import, unicode_literals

from django.contrib.auth import get_user_model
from souvenirs.control import count_active_users
from souvenirs.models import Souvenir
from souvenirs.reports import _usage_for_periods


def usage_for_periods(periods):
    """
    Augment django-souvenirs's usage_for_periods with learners and staff.

    django-souvenirs uses this wrapper via
    settings.SOUVENIRS_USAGE_REPORTS_FUNCTION

    """
    for d in _usage_for_periods(periods):
        d['usage'].update(registered_learners_and_staff_as_of(d['period']['end']))
        d['usage'].update(count_active_learners_and_staff(start=d['period']['start'],
                                                          end=d['period']['end']))
        yield d


def registered_learners_and_staff_as_of(date):
    """
    Return a dict counting the registered learners and staff as of the given
    date. See also souvenirs.reports.registered_users_as_of
    """
    User = get_user_model()
    users = User.objects.filter(date_joined__lt=date)
    learners = users.filter(is_staff=False)
    staff = users.filter(is_staff=True)
    return dict(
        registered_learners=learners.count(),
        activated_learners=learners.filter(is_active=True).count(),
        registered_staff=staff.count(),
        activated_staff=staff.filter(is_active=True).count(),
    )


def count_active_learners_and_staff(start=None, end=None):
    """
    Return a dict counting the active learners and staff between start and end
    datetimes, inclusive and exclusive respectively.
    """
    qs = Souvenir.objects.all()
    return dict(
        active_learners=count_active_users(start, end, qs=qs.filter(user__is_staff=False)),
        active_staff=count_active_users(start, end, qs=qs.filter(user__is_staff=True)),
    )
