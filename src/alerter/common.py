import logging
import yaml

from abc import ABC, abstractmethod
from collections.abc import Callable

class Alerter(ABC, Callable):
    # add the rest here
