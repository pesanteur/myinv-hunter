import alerter.discord
import alerter.emailer
import alerter.slack
import alerter.telegram # figure out setting up hooks with telegram and slack

from alerter.common import AlerterFactory


def init_alerters(args):
    return AlerterFactory.create(args)
