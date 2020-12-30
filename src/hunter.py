import logging
import sched
import smtplib
import sys

from email.message import EmailMessage
from email.utils import formatdate
from scraper import Scraper

class Alerter:
    def __init__(self, args):
        self.sender
