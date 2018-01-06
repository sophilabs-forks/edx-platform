# -*- coding: utf-8 -*-
"""
A diagnostic utility that can be used to render email messages to files on disk.
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
from edx_ace.channel import Channel, ChannelType

LOG = logging.getLogger(__name__)


class DjangoEmailChannel(Channel):
    # """
    # An email channel that simply renders the message HTML to a file and the body text to stdout.
    # If you add this channel to your enabled channels list as your email channel, it will write out the text version
    # of the email to stdout and the HTML version to an output file.
    # Examples::
    #     ACE_ENABLED_CHANNELS = ['file_email']
    # By default it writes the output file to /edx/src/ace_output.html and overwrites any existing file at that location.
    # In the edX devstack, this folder is shared between the host and the containers so you can easily open the file using
    # a browser on the host. You can override this output file location by passing in a ``output_file_path`` key in the
    # message context. That path specifies where in the container filesystem the file should be written.
    # Both streams of output are UTF-8 encoded.
    # """

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
