from pkg_resources import (  # type: ignore[import-untyped]
    DistributionNotFound,
    get_distribution,
)

from . import criteria as criteria
from .api import ApiInsee as ApiInsee

try:
    dist_name = __name__
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = "unknown"
finally:
    del get_distribution, DistributionNotFound
