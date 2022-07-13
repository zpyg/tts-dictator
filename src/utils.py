import sys
import logging

from tenacity import retry as _retry
from tenacity import wait_fixed, after_log

logging.basicConfig(stream=sys.stderr, level=logging.WARNING)

logger = logging.getLogger(__name__)

retry = _retry(wait=wait_fixed(3), after=after_log(logger, logging.WARNING))
