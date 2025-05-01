from app.commands.command_base import Command

class DivideCommand(Command):
    """Command to perform division."""

    def __init__(self, *args):
        self.numbers = list(map(float, args))

    def execute(self):
        if not self.numbers:
            raise ValueError("No numbers provided for division.")
        result = self.numbers[0]
        for n in self.numbers[1:]:
            if n == 0:
                raise ZeroDivisionError("Cannot divide by zero.")
            result /= n
        return result
