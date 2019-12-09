# future imports
from __future__ import absolute_import
from __future__ import unicode_literals

# stdlib imports
import logging
import time

# third-party imports
import pykka

# local imports
from ..utils import send_webhook


logger = logging.getLogger(__name__)


class StatusReporter(pykka.ThreadingActor):
    """Periodically sends webhook notifications to the configured server
    containing data on the player's current status.
    """

    def __init__(self, config, core):
        super(StatusReporter, self).__init__()
        self.config = config['webhooks']
        self.core = core
        self.in_future = self.actor_ref.proxy()

    def on_receive(self, message):
        logger.info("StatusReporter got: " + message)
