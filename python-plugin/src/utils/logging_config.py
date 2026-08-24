"""Logging configuration for the Python plugin."""

import logging


def configure_logging() -> None:
    """Configure a simple application-wide logging format."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
