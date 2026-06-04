"""Phase 0 acceptance tests: Logging setup."""

import logging


def test_logger_returns_logger_instance():
    """setup_logger must return a valid logging.Logger."""
    from core.logger import setup_logger
    logger = setup_logger("test_module")
    assert isinstance(logger, logging.Logger)


def test_logger_has_handler():
    """Logger must have at least one handler configured."""
    from core.logger import setup_logger
    logger = setup_logger("test_handler_module")
    assert len(logger.handlers) > 0


def test_logger_respects_name():
    """Logger name must match the requested name."""
    from core.logger import setup_logger
    logger = setup_logger("my_custom_name")
    assert logger.name == "my_custom_name"
