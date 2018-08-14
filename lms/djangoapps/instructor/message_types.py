"""
ACE message types for the instructor module.
"""

from openedx.core.djangoapps.ace_common.message import BaseMessageType


class AddBetaTester(BaseMessageType):
    """
    A message for beta students when they're invited.
    """
    APP_LABEL = 'instructor'

    def __init__(self, *args, **kwargs):
        super(AddBetaTester, self).__init__(*args, **kwargs)
        self.options['transactional'] = True  # pylint: disable=unsupported-assignment-operation


class AllowedEnroll(BaseMessageType):
    """
    A message for _unregistered_ students who received an invitation to a course.
    """
    APP_LABEL = 'instructor'

    def __init__(self, *args, **kwargs):
        super(AllowedEnroll, self).__init__(*args, **kwargs)
        self.options['transactional'] = True  # pylint: disable=unsupported-assignment-operation


class AllowedUnenroll(BaseMessageType):
    """
    A message for _unregistered_ students who had their invitation to a course cancelled.
    """
    APP_LABEL = 'instructor'

    def __init__(self, *args, **kwargs):
        super(AllowedUnenroll, self).__init__(*args, **kwargs)
        self.options['transactional'] = True  # pylint: disable=unsupported-assignment-operation


class EnrollEnrolled(BaseMessageType):
    """
    A message for _registered_ students who have been both invited and enrolled to a course.
    """
    APP_LABEL = 'instructor'

    def __init__(self, *args, **kwargs):
        super(EnrollEnrolled, self).__init__(*args, **kwargs)
        self.options['transactional'] = True  # pylint: disable=unsupported-assignment-operation


class EnrolledUnenroll(BaseMessageType):
    """
    A message for _registered_ students who have been unenrolled from a course.
    """
    APP_LABEL = 'instructor'

    def __init__(self, *args, **kwargs):
        super(EnrolledUnenroll, self).__init__(*args, **kwargs)
        self.options['transactional'] = True  # pylint: disable=unsupported-assignment-operation
