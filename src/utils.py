from tenacity import retry as _retry
from tenacity import stop_after_attempt, wait_fixed

retry = _retry(stop=stop_after_attempt(2), wait=wait_fixed(2))
