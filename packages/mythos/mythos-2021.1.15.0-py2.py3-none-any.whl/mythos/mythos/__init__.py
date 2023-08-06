import logging

from .__version__ import __version__  # noqa


# Default logging handler to avoid "No handler found" warnings.
logging.getLogger("mythos").addHandler(logging.NullHandler())
