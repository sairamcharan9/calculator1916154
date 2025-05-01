from app.commands.command_base import Command

class SubtractCommand(Command):
    """Command to perform subtraction."""

    def __init__(self, *args):
        self.numbers = list(map(float, args))

    def execute(self):
        if not self.numbers:
            raise ValueError("No numbers provided for subtraction.")
        result = self.numbers[0]
        for n in self.numbers[1:]:
            result -= n
        return result
