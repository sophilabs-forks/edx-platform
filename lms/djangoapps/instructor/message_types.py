"""
ACE message types for the student module.
"""

from openedx.core.djangoapps.ace_common.message import BaseMessageType


class EnrollEnrolled(BaseMessageType):
    def __init__(self, *args, **kwargs):
        super(EnrollEnrolled, self).__init__(*args, **kwargs)

        self.options['transactional'] = True
