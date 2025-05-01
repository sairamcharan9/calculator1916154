from app.commands.command_base import Command

class MultiplyCommand(Command):
    """Command to perform multiplication."""

    def __init__(self, *args):
        self.numbers = list(map(float, args))

    def execute(self):
        if not self.numbers:
            raise ValueError("No numbers provided for multiplication.")
        result = 1.0
        for n in self.numbers:
            result *= n
        return result
