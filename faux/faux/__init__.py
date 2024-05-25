import logging
import logging.config
import os


def configure_logging():
    log_level = os.getenv("LOG_LEVEL", "INFO")
    log_format = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"

    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[logging.StreamHandler()],
    )


# Configure logging for the package
configure_logging()

# Create a logger for this package
logger = logging.getLogger(__name__)
logger.info("Logging is configured for faux package")
