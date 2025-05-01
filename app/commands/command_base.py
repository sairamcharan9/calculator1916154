from abc import ABC, abstractmethod

class Command(ABC):
    """Abstract base class for all calculator commands."""

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass
