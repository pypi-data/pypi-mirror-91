from .User import *
from .Service import *
from . import ServiceException
from .Token import *
from .Informations import *
import RDS.Util as Util


def int_or_str(value):
    try:
        return int(value)
    except TypeError:
        return value


__version__ = "0.21"
VERSION = tuple(map(int_or_str, __version__.split(".")))

__all__ = [
    "User",
    "Service",
    "OAuth2Service",
    "Token",
    "OAuth2Token",
    "Util",
    "ServiceException",
    "LoginMode",
    "FileTransferMode"
]

