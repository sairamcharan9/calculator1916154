"""
Logger configuration for the calculator application.
Provides flexible logging configuration and integration with environment variables.
"""

import logging
import logging.config
import os
import sys
from dotenv import load_dotenv
from typing import Optional

# Load environment variables from .env file if it exists
load_dotenv()

class LoggerConfig:
    """Singleton class to configure logging for the calculator application."""
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        """Ensure only one instance of LoggerConfig exists (Singleton pattern)."""
        if cls._instance is None:
            cls._instance = super(LoggerConfig, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    @classmethod
    def reset(cls):
        """
        Reset the singleton instance for testing purposes.
        """
        cls._instance = None

    def __init__(self):
        """Initialize logger configuration if not already initialized."""
        if self._initialized:
            return
        self._initialized = True
        self.logger = logging.getLogger('calculator')
        self.configure()

    def configure(self, log_level: Optional[str] = None, log_file: Optional[str] = None):
        """
        Configure the logger based on environment variables or provided parameters.
        
        Args:
            log_level (str, optional): Log level to use ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
            log_file (str, optional): Path to log file
        """
        # First try to use logging.conf if it exists and not in testing environment
        if os.environ.get("ENVIRONMENT") != "testing":
            logging_conf_path = os.path.join(os.getcwd(), 'logging.conf')
            if os.path.exists(logging_conf_path):
                try:
                    # Configure logging using the config file
                    logging.config.fileConfig(logging_conf_path, disable_existing_loggers=False)
                    # After fileConfig, re-fetch the logger to ensure new config is used
                    self.logger = logging.getLogger('calculator')
                    self.logger.info("Logging configured using logging.conf")
                    return
                except Exception as e:
                    # Fall back to manual configuration if there's an issue
                    self.logger = logging.getLogger('calculator')
                    self.logger.error(f"Error loading logging.conf: {e}")

        # Get log level from parameter, environment variable, or use default
        if log_level is None:
            log_level = os.getenv('LOG_LEVEL', 'INFO').upper()

        # Map string log level to logging constant
        numeric_level = getattr(logging, log_level.upper(), logging.INFO)

        # Get log file path from parameter, environment variable, or use default
        if log_file is None:
            log_file = os.getenv('LOG_FILE', 'logs/app.log')

        # Make sure logs directory exists
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Remove all handlers from root logger and calculator logger to avoid duplication
        root_logger = logging.getLogger()
        for handler in list(root_logger.handlers):
            root_logger.removeHandler(handler)
        for handler in list(self.logger.handlers):
            self.logger.removeHandler(handler)

        # Remove all handlers from root logger to avoid basicConfig no-op
        root_logger = logging.getLogger()
        for handler in list(root_logger.handlers):
            root_logger.removeHandler(handler)

        # Configure root logger with handlers
        logging.basicConfig(
            level=numeric_level,
            format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )

        # Explicitly set level for all handlers on root logger
        for handler in logging.getLogger().handlers:
            handler.setLevel(numeric_level)
        # Set level for calculator logger
        self.logger.setLevel(numeric_level)
        self.logger.propagate = True
        # Also set root logger level
        logging.getLogger().setLevel(numeric_level)

        self.logger.info(f"Logger configured with level={log_level}, file={log_file}")

    def get_logger(self, name: Optional[str] = None) -> logging.Logger:
        """
        Get a logger instance.
        
        Args:
            name (str, optional): Logger name suffix
            
        Returns:
            logging.Logger: Logger instance
        """
        if name:
            logger = logging.getLogger(f'calculator.{name}')
            # Ensure level is set; let it propagate to parent
            logger.setLevel(self.logger.level)
            logger.propagate = True
            return logger
        return self.logger


# Singleton instance to access throughout application
logger_config = LoggerConfig()

def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a logger instance.
    
    Args:
        name (str, optional): Logger name suffix
        
    Returns:
        logging.Logger: Logger instance
    """
    return logger_config.get_logger(name)
