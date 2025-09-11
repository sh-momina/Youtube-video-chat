# cookies_helper.py
import os
import base64
import logging

logger = logging.getLogger("cookies_helper")

def ensure_cookies_file(path="cookies.txt"):
    """
    Create cookies.txt from environment if not present.
    Supports:
      - YTDLP_COOKIES       (raw multi-line cookies.txt)
      - YTDLP_COOKIES_B64   (base64-encoded cookies.txt)
    Returns path if available, otherwise None.
    """
    if os.path.exists(path):
        logger.info(f"{path} already exists")
        return path

    raw = os.getenv("YTDLP_COOKIES")
    b64 = os.getenv("YTDLP_COOKIES_B64")

    if raw:
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(raw)
            logger.info(f"Wrote cookies file from YTDLP_COOKIES to {path}")
            return path
        except Exception as e:
            logger.exception("Failed writing raw cookies")
            return None

    if b64:
        try:
            data = base64.b64decode(b64)
            with open(path, "wb") as f:
                f.write(data)
            logger.info(f"Wrote cookies file from YTDLP_COOKIES_B64 to {path}")
            return path
        except Exception as e:
            logger.exception("Failed decoding/writing base64 cookies")
            return None

    logger.info("No cookie env var found")
    return None
