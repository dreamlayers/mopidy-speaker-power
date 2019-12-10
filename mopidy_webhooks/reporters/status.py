# future imports
from __future__ import absolute_import
from __future__ import unicode_literals

# stdlib imports
import logging
import threading

# third-party imports
import pykka
from mopidy.audio import PlaybackState

# local imports
from ..utils import send_webhook


logger = logging.getLogger(__name__)


class StatusReporter(pykka.ThreadingActor):
    """Periodically sends webhook notifications to the configured server
    containing data on the player's current status.
    """

    def _timeout(self):
        self.actor_ref.tell("timeout")

    def _start_timer(self, time):
        if self.timer:
            self.timer.cancel()
        self.timer = threading.Timer(time, self._timeout)
        self.timer.start()

    def _on_timeout(self):
        self.timer = None
        if not self.playing:
            send_webhook(self.config, False)

    def _on_stop(self):
        if self.playing:
            self.playing = False
            self._start_timer(self.stop_timeout)

    def _on_pause(self):
        if self.playing:
            self.playing = False
            self._start_timer(self.pause_timeout)

    def _on_play(self):
        if self.timer:
            self.timer.cancel()
            self.timer = None

        if not self.playing:
            send_webhook(self.config, True)
            self.playing = True

    def __init__(self, config):
        super(StatusReporter, self).__init__()
        self.playing = False
        self.timer = None
        self.config = config
        self.pause_timeout = config['pause_timeout']
        self.stop_timeout = config['stop_timeout']
        self.fnmap = { "timeout": self._on_timeout,
                       PlaybackState.STOPPED: self._on_stop,
                       PlaybackState.PAUSED: self._on_pause,
                       PlaybackState.PLAYING: self._on_play }

    def on_receive(self, message):
        func = self.fnmap.get(message)
        if func:
            func()
        else:
            logger.error("StatusReporter has no action for: " + message)

    def on_stop(self):
        if self.timer:
            self.timer.cancel()

        if self.playing or self.timer:
            send_webhook(self.config, False)

        self.playing = False
        self.timer = None
