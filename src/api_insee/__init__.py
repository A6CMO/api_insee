from pkg_resources import (
    DistributionNotFound,
    get_distribution,
)

from . import criteria as criteria
from .api import ApiInsee as ApiInsee
from .conf import ApiVersion as ApiVersion

try:
    dist_name = __name__
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:  # pragma: no cover
    __version__ = "unknown"
finally:
    del get_distribution, DistributionNotFound
