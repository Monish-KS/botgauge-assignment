import random
import time
from typing import Callable, TypeVar

T = TypeVar("T")


def with_retry(
    fn: Callable[[], T],
    max_attempts: int = 5,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    get_retry_after: Callable[[], float | None] | None = None,
) -> T:
    last_error = None
    for attempt in range(max_attempts):
        try:
            return fn()
        except Exception as e:
            last_error = e
            if attempt == max_attempts - 1:
                raise
            wait = base_delay * (2 ** attempt)
            if get_retry_after is not None:
                ra = get_retry_after()
                if ra is not None and ra > 0:
                    wait = min(ra, max_delay)
            jitter = random.uniform(0, wait * 0.2)
            time.sleep(wait + jitter)
    raise last_error
