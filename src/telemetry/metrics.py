import time
import logging
from contextlib import contextmanager

logger = logging.getLogger("metrics")
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")

@contextmanager
def timed(label: str):
    t0 = time.perf_counter()
    try:
        yield
    finally:
        dt = (time.perf_counter() - t0) * 1000
        logger.info(f"{label} | latency_ms={dt:.1f}")

class Counters: # can alo extend for API usage cost if we move with paid LLM
    llm_tokens_in = 0
    llm_tokens_out = 0

COUNTERS = Counters()