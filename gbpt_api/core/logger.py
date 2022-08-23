import logging
import logging.config
import os
from pathlib import Path

import yaml  # type: ignore


def configure_logger():
    config_path = os.getenv(
        "APP_LOG_CONFIG_PATH", Path(__file__).parent / "etc" / "logging.yaml"
    )

    with open(config_path, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        logging.config.dictConfig(config)


def get_logger(name: str) -> logging.Logger:
    """Retrieve a logger.

    Args:
        name: The name of the logger.

    Returns:
        A standard library logging.Logger logger.
    """
    return logging.getLogger(name)
