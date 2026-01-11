"""
Logging configuration for Varinaut API.

Provides a unified logging setup with:
- Rotating file handler (prevents unbounded log growth)
- Console output for development
- Consistent formatting across all modules
"""

import logging
import logging.handlers
from pathlib import Path


def setup_logging(
    log_dir: Path = Path("logs"),
    log_level: int = logging.INFO,
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5,
) -> None:
    """
    Configure application-wide logging.

    Args:
        log_dir: Directory for log files (created if doesn't exist)
        log_level: Minimum log level to capture
        max_bytes: Max size per log file before rotation
        backup_count: Number of rotated files to keep
    """
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "varinaut.log"

    # Format: timestamp | level | logger name | message
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Rotating file handler
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)

    # Console handler for development
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    # Quiet down noisy third-party libraries
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

    # Log startup message
    logger = logging.getLogger("varinaut")
    logger.info("Logging initialized: level=%s, file=%s", logging.getLevelName(log_level), log_file)
