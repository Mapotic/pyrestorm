"""Top-level package for PyRestORM."""

__author__ = """Martin Kubát"""
__email__ = 'martin.kubat@mapotic.com'
__version__ = '0.1.0'

from .manager import BaseRESTManager
from .model import BaseRESTModel
from .http import HttpExceptionError