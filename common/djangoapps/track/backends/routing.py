from analytics import Client
from eventtracking.backends.segment import SegmentBackend as BaseSegmentBackend

import logging

from track.backends import BaseBackend

log = logging.getLogger('track.backends.logger')


class SegmentBackend(BaseSegmentBackend, BaseBackend):
    def __init__(self, **kwargs):
        self.blacklist = kwargs.get('blacklist', [])

    def send(self, event):
        event_name = event.get('name')
        if event_name and event_name in self.blacklist:
            return

        super(SegmentBackend, self).send(event)


class SiteSegmentBackend(BaseSegmentBackend, BaseBackend):
    def __init__(self, **kwargs):
        """Event tracker backend that uses a python logger.

        :Parameters:
          - `name`: identifier of the logger, which should have
            been configured using the default python mechanisms.

        """
        super(CustomSegmentBackend, self).__init__()
        self.event_logger = logging.getLogger('segment_override')

        self.custom_segment = Client(
            write_key=SAMPLE_KEY,
            debug=False, on_error=None, send=True
        )


    def get_site_segment_key(self):
        """
        Get the current site configuration to see if there is a custom key
        configured
        :return: Segment IO write key
        """
        return SAMPLE_KEY

    def send(self, event):
        """
        Process the event using all registered processors and send it to all registered backends.
        Logs and swallows all `Exception`.
        """
        context = event.get('context', {})
        user_id = context.get('user_id')
        name = event.get('name')
        if name is None or user_id is None:
            return

        segment_context = {}

        # TODO Should be grabbed from the site config
        ga_client_id = context.get('client_id')
        if ga_client_id is not None:
            segment_context['Google Analytics'] = {
                'clientId': ga_client_id
            }

        # TODO Grab the proper type from the event
        self.custom_segment.track(
            user_id,
            name,
            event,
            context=segment_context
        )
