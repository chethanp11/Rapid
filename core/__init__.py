# RAPID Core Package
__version__ = "1.0.0"

import logging

logger = logging.getLogger("rapid.core")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[RAPID] %(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)