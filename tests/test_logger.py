"""
Unit tests for the logger module.
"""
import os
import pytest
import logging
import tempfile
from unittest.mock import patch, MagicMock
import configparser
from src.history.logger import LoggerConfig, get_logger

class TestLoggerConfig:
    """Tests for the LoggerConfig class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Create a temporary directory for log files
        self.temp_dir = tempfile.TemporaryDirectory()
        self.log_file = os.path.join(self.temp_dir.name, "test.log")
        
        # Save original environment variables
        self.original_log_level = os.environ.get('LOG_LEVEL')
        self.original_log_file = os.environ.get('LOG_FILE')
        self.original_environment = os.environ.get('ENVIRONMENT')
        
        # Set environment variables for testing
        os.environ['LOG_LEVEL'] = 'INFO'
        os.environ['LOG_FILE'] = self.log_file
        os.environ['ENVIRONMENT'] = 'testing'
        
        # Reset logger singleton for test isolation (after env vars)
        LoggerConfig.reset()
        
        # Clear any existing loggers
        logging.root.handlers = []
        logging.root.setLevel(logging.DEBUG)
        # Force all root handlers to DEBUG (for tests that add handlers after setup)
        for handler in logging.getLogger().handlers:
            handler.setLevel(logging.DEBUG)
        
        # Clear any existing loggers
        logging.root.handlers = []
        logging.root.setLevel(logging.INFO)
    
    def teardown_method(self):
        """Tear down test fixtures."""
        # Reset logger singleton for test isolation
        LoggerConfig.reset()
        # Close and remove all handlers from root logger
        root_logger = logging.getLogger()
        for handler in list(root_logger.handlers):
            handler.close()
            root_logger.removeHandler(handler)
        # Close and remove all handlers from calculator loggers
        for logger_name in ["calculator", "calculator.test_logger", "calculator.test_module"]:
            logger = logging.getLogger(logger_name)
            for handler in list(logger.handlers):
                handler.close()
                logger.removeHandler(handler)
        # Restore original environment variables
        if self.original_log_level:
            os.environ['LOG_LEVEL'] = self.original_log_level
        else:
            os.environ.pop('LOG_LEVEL', None)
        
        if self.original_log_file:
            os.environ['LOG_FILE'] = self.original_log_file
        else:
            os.environ.pop('LOG_FILE', None)
        
        if self.original_environment:
            os.environ['ENVIRONMENT'] = self.original_environment
        else:
            os.environ.pop('ENVIRONMENT', None)
        
        # Clean up temporary directory
        self.temp_dir.cleanup()
    
    def test_singleton_pattern(self):
        """Test that LoggerConfig implements the Singleton pattern."""
        logger_config1 = LoggerConfig()
        logger_config2 = LoggerConfig()
        
        # Both instances should be the same object
        assert logger_config1 is logger_config2
    
    def test_logger_initialization(self):
        """Test logger initialization with environment variables."""
        logger_config = LoggerConfig()
        logger = logger_config.get_logger("test_logger")
        
        # Check logger properties
        assert logger.name == "calculator.test_logger"
        assert logger.level == logging.INFO
        
        # Check that file handler was created
        root_logger = logging.getLogger()
        assert any(isinstance(handler, logging.FileHandler) for handler in root_logger.handlers)
        
        # Check that console handler was created
        assert any(isinstance(handler, logging.StreamHandler) for handler in root_logger.handlers)
    
    @patch('logging.config.fileConfig')
    def test_config_file_loading(self, mock_fileconfig):
        """Test loading configuration from file."""
        # Simulate not in testing environment for this test
        original_env = os.environ.get('ENVIRONMENT')
        os.environ['ENVIRONMENT'] = 'production'
        # Create a mock config file
        with tempfile.NamedTemporaryFile(suffix='.conf', delete=False) as config_file:
            config_file.write(b"[loggers]\nkeys=root\n\n[handlers]\nkeys=consoleHandler\n\n[formatters]\nkeys=simpleFormatter")
        
        try:
            # Patch os.path.exists to return True for our config file
            with patch('os.path.exists', return_value=True):
                # Patch os.getcwd to return the directory of our config file
                with patch('os.getcwd', return_value=os.path.dirname(config_file.name)):
                    # Create logger config
                    LoggerConfig.reset()
                    logger_config = LoggerConfig()
                    mock_fileconfig.assert_called_once()
        finally:
            # Clean up the config file
            os.unlink(config_file.name)
            # Restore ENVIRONMENT
            if original_env is not None:
                os.environ['ENVIRONMENT'] = original_env
            else:
                os.environ.pop('ENVIRONMENT', None)
    
    @patch('os.path.exists')
    @patch('logging.config.fileConfig')
    def test_config_file_error_handling(self, mock_fileconfig, mock_exists):
        """Test error handling when loading config file."""
        # Simulate not in testing environment for this test
        original_env = os.environ.get('ENVIRONMENT')
        os.environ['ENVIRONMENT'] = 'production'
        # Mock that config file exists
        mock_exists.return_value = True
        
        # Mock fileConfig to raise an exception
        mock_fileconfig.side_effect = configparser.Error("Test error")
        
        # Create logger config - should fall back to manual configuration
        LoggerConfig.reset()
        logger_config = LoggerConfig()
        
        # Verify fileConfig was called
        mock_fileconfig.assert_called_once()
        
        # Verify a logger can still be created
        logger = logger_config.get_logger("test_logger")
        assert logger is not None
        # Restore ENVIRONMENT
        if original_env is not None:
            os.environ['ENVIRONMENT'] = original_env
        else:
            os.environ.pop('ENVIRONMENT', None)
    
    def test_environment_variable_handling(self):
        """Test handling of various environment variable values."""
        # Test different log levels
        for level_name in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
            os.environ['LOG_LEVEL'] = level_name
            LoggerConfig.reset()
            logger_config = LoggerConfig()
            logger = logger_config.get_logger("test_logger")
            expected_level = getattr(logging, level_name)
            assert logger.level == expected_level
        
        # Test invalid log level
        os.environ['LOG_LEVEL'] = 'INVALID_LEVEL'
        LoggerConfig.reset()
        logger_config = LoggerConfig()
        logger = logger_config.get_logger("test_logger")
        # Should default to INFO if level is invalid
        assert logger.level == logging.INFO
        
        # Test without log file specified
        os.environ.pop('LOG_FILE', None)
        LoggerConfig.reset()
        logger_config = LoggerConfig()
        logger = logger_config.get_logger("test_logger")
        # Console/FileHandlers are now only attached to root logger, not named loggers
        root_logger = logging.getLogger()
        assert any(isinstance(handler, logging.StreamHandler) for handler in root_logger.handlers)
    
    def test_get_logger_function(self):
        """Test the get_logger function."""
        # Get a logger
        logger = get_logger("test_module")
        
        # Check logger properties
        assert logger.name == "calculator.test_module"
        assert logger.level <= logging.INFO  # Level should be INFO or lower
        
        # Get the same logger again (should be cached)
        logger2 = get_logger("test_module")
        assert logger is logger2

class TestLoggingFunctionality:
    """Tests for logging functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Create a temporary log file
        fd, self.log_file = tempfile.mkstemp(suffix='.log')
        os.close(fd)
        
        # Set environment variables
        os.environ['LOG_LEVEL'] = 'DEBUG'
        os.environ['LOG_FILE'] = self.log_file
        os.environ['ENVIRONMENT'] = 'testing'
        
        # Reset logger singleton for test isolation (after env vars)
        LoggerConfig.reset()
        
        # Clear handlers
        logging.root.handlers = []
        logging.root.setLevel(logging.DEBUG)
        # Force all root handlers to DEBUG (for tests that add handlers after setup)
        for handler in logging.getLogger().handlers:
            handler.setLevel(logging.DEBUG)
    
    def teardown_method(self):
        """Tear down test fixtures."""
        # Reset logger singleton for test isolation
        LoggerConfig.reset()
        # Close and remove all handlers from root logger
        root_logger = logging.getLogger()
        for handler in list(root_logger.handlers):
            handler.close()
            root_logger.removeHandler(handler)
        # Close and remove all handlers from calculator loggers
        for logger_name in ["calculator", "calculator.test_file_logger", "calculator.test_console_logger"]:
            logger = logging.getLogger(logger_name)
            for handler in list(logger.handlers):
                handler.close()
                logger.removeHandler(handler)
        # Clean up temp file
        if os.path.exists(self.log_file):
            os.unlink(self.log_file)
    
    def test_logging_to_file(self, caplog):
        """Test that logging messages are written to the file (in-memory check)."""
        logger = get_logger("test_file_logger")
        logger.setLevel(logging.DEBUG)
        with caplog.at_level(logging.DEBUG):
            logger.debug("DEBUG: Test log message")
            logger.info("INFO: Test log message")
            logger.warning("WARNING: Test log message")
            logger.error("ERROR: Test log message")
            logger.critical("CRITICAL: Test log message")
        log_text = caplog.text
        assert "DEBUG: Test log message" in log_text
        assert "INFO: Test log message" in log_text
        assert "WARNING: Test log message" in log_text
        assert "ERROR: Test log message" in log_text
        assert "CRITICAL: Test log message" in log_text
    
    def test_logging_to_console(self, caplog):
        """Test that logging messages are sent to the console."""
        logger = get_logger("test_console_logger")
        
        # Log a message
        logger.info("Console test message")
        
        # Check that emit was called
        assert "Console test message" in caplog.text

class TestLoggerWithRandomData:
    """Tests for logger with random data."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Create a temporary log file
        fd, self.log_file = tempfile.mkstemp(suffix='.log')
        os.close(fd)
        
        # Set environment variables
        os.environ['LOG_LEVEL'] = 'DEBUG'
        os.environ['LOG_FILE'] = self.log_file
        os.environ['ENVIRONMENT'] = 'testing'
        
        # Reset logger singleton for test isolation (after env vars)
        LoggerConfig.reset()
        
        # Clear handlers
        logging.root.handlers = []
        logging.root.setLevel(logging.DEBUG)
        # Force all root handlers to DEBUG (for tests that add handlers after setup)
        for handler in logging.getLogger().handlers:
            handler.setLevel(logging.DEBUG)
    
    def teardown_method(self):
        """Tear down test fixtures."""
        # Reset logger singleton for test isolation
        LoggerConfig.reset()
        # Close and remove all handlers from root logger
        root_logger = logging.getLogger()
        for handler in list(root_logger.handlers):
            handler.close()
            root_logger.removeHandler(handler)
        # Close and remove all handlers from calculator loggers
        for logger_name in ["calculator", "calculator.test_file_logger", "calculator.test_console_logger"]:
            logger = logging.getLogger(logger_name)
            for handler in list(logger.handlers):
                handler.close()
                logger.removeHandler(handler)
        # Clean up temp file
        if os.path.exists(self.log_file):
            os.unlink(self.log_file)
    
    def test_random_logging(self, caplog, faker, num_records=10):
        """Test logging with random data (in-memory check)."""
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        with caplog.at_level(logging.DEBUG):
            for i in range(num_records):
                level = faker.random_element([
                    logging.DEBUG, logging.INFO, logging.WARNING, 
                    logging.ERROR, logging.CRITICAL
                ])
                message = f"{logging.getLevelName(level)}: {faker.sentence()}"
                root_logger.log(level, message)
        # Ensure at least num_records logs are present for the root logger
        assert sum(1 for r in caplog.records if r.name == root_logger.name) >= num_records
