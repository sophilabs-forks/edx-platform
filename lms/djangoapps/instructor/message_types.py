"""
ACE message types for the instructor module.
"""

from openedx.core.djangoapps.ace_common.message import BaseMessageType


class EnrollEnrolled(BaseMessageType):
    """
    A message for _registered_ students who are invited to a course and got successfully enrolled in.
    """
    APP_LABEL = 'instructor'

    def __init__(self, *args, **kwargs):
        super(EnrollEnrolled, self).__init__(*args, **kwargs)
        self.options['transactional'] = True  # pylint: disable=unsupported-assignment-operation
