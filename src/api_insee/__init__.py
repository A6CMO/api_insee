# -*- coding: utf-8 -*-
from pkg_resources import DistributionNotFound, get_distribution

from .api import ApiInsee

try:
    dist_name = __name__
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = "unknown"
finally:
    del get_distribution, DistributionNotFound
