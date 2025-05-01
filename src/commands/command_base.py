"""
Command base class for the calculator command pattern implementation.
"""

from abc import ABC, abstractmethod
from typing import Any

class Command(ABC):
    """Abstract base class for all calculator commands."""

    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        """
        Execute the command with the given arguments.
        
        Args:
            *args: Positional arguments for the command
            **kwargs: Keyword arguments for the command
            
        Returns:
            Any: Result of command execution
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Return the command name (for registration/discovery).
        
        Returns:
            str: The name of the command
        """
        pass
