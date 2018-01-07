# -*- coding: utf-8 -*-
"""
A diagnostic utility that can be used to render email messages to files on disk.
"""
from django.conf import settings
from django.core import mail
from edx_ace.channel import Channel, ChannelType
import logging
import re

from openedx.core.djangoapps.site_configuration import helpers as configuration_helpers


LOG = logging.getLogger(__name__)


class DjangoEmailChannel(Channel):
    """
    A `send_mail` interface for edX ACE.

    This is both useful for debugging ACE mail by inspecting `django.core.mail.outbox`, and for providing an
    alternative to Sailthru.

    TODO: Move to `edx-ace`.
    """

    channel_type = ChannelType.EMAIL

    @classmethod
    def enabled(cls):
        """
        Returns: True always!
        """
        return True

    def deliver(self, message, rendered_message):
        # Compress spaces and remove newlines to make it easier to author templates.
        subject = re.sub('\s+', ' ', rendered_message.subject).strip()

        mail.send_mail(
            subject,
            rendered_message.body,
            configuration_helpers.get_value('email_from_address', settings.DEFAULT_FROM_EMAIL),
            [message.recipient.email_address],
            html_message=rendered_message.body_html,  # TODO: Fill out Sailthru specific variables
        )
