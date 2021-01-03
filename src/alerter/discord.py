import logging
import requests
import traceback

from alerter.common import Alerter, AlerterFactory


@AlerterFactory.register
class DiscordAlerter(Alerter):
    # add the rest here
