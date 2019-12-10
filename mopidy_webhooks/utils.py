# future imports
from __future__ import unicode_literals

# stdlib imports
import json
import logging

# third-party imports
import requests
from mopidy.models import ModelJSONEncoder

logger = logging.getLogger(__name__)


def send_webhook(config, on):
    """Sends a HTTP request to the configured server.

    All exceptions are suppressed but emit a warning message in the log.
    """
    try:
        response = requests.post(
            config['hass_url'] + "/api/services/switch/" +
                ("turn_on" if on else "turn_off"),
            data='{"entity_id": "switch.' + config['switch_name'] + '"}',
            headers={"Authorization": config['api_key']},
        )
    except Exception as e:
        logger.warning('Webhook fail')
