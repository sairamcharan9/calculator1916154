from app.commands.command_base import Command

class ExitCommand(Command):
    """Command to exit the calculator REPL."""
    def __init__(self, *args):
        self.numbers = list(args)  # for compatibility, but not used
    def execute(self):
        import sys
        sys.exit(0)
