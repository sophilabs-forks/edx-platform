# -*- coding: utf-8 -*-
"""
A diagnostic utility that can be used to render email messages to files on disk.
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
from edx_ace.channel import Channel, ChannelType

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
        from edx_ace import MessageType
        from django.conf import settings
        from openedx.core.djangoapps.site_configuration import helpers as configuration_helpers

        message = MessageType()  # TODO: Comment this out when done

        from django.core.mail import send_mail
        send_mail(
            subject=rendered_message['subject'],
            message=rendered_message['body'],
            from_email=configuration_helpers.get_value('email_from_address', settings.DEFAULT_FROM_EMAIL),
            recipient_list=[message.recipient.email_address],
            html_message=rendered_message['body_html'],  # TODO: Fill out Sailthru specific variables
        )
