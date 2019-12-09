# future imports
from __future__ import absolute_import
from __future__ import unicode_literals

# stdlib imports
import logging

# third-party imports
import pykka
from mopidy.core import CoreListener

# local imports
from ..utils import send_webhook


logger = logging.getLogger(__name__)


class EventReporter(pykka.ThreadingActor, CoreListener):

    def __init__(self, config, status_reporter):
        super(EventReporter, self).__init__()
        self.status_reporter = status_reporter
        self.config = config['webhooks']

    def on_start(self):
        logger.info('EventReporter started.')

    def playback_state_changed(self, old_state, new_state):
        #send_webhook(self.config, new_state)
        logger.info(new_state)
        self.status_reporter.tell(new_state)
