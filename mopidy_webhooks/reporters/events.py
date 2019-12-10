# future imports
from __future__ import absolute_import
from __future__ import unicode_literals

# third-party imports
import pykka
from mopidy.core import CoreListener

# local imports
from ..utils import send_webhook


class EventReporter(pykka.ThreadingActor, CoreListener):

    def __init__(self, status_reporter):
        super(EventReporter, self).__init__()
        self.status_reporter = status_reporter

    def playback_state_changed(self, old_state, new_state):
        self.status_reporter.tell(new_state)
