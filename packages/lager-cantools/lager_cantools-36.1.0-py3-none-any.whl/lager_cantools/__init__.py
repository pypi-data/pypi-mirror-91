import sys
import argparse

from . import tester
from . import j1939
from .errors import Error

# Remove once less users are using the old package structure.
from . import database as db

from .version import __version__

__author__ = 'Erik Moqvist'
