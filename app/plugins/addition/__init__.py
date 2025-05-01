from app.commands.command_base import Command

class AddCommand(Command):
    """Command to perform addition."""

    def __init__(self, *args):
        self.numbers = list(map(float, args))

    def execute(self):
        return sum(self.numbers)