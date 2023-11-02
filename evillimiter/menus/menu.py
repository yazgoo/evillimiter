import enum
import collections

from .parser import CommandParser
from evillimiter.console.io import IO

from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

class CommandMenu(object):
    def __init__(self):
        self.commands = []
        self.prompt = '>>> '
        self.parser = CommandParser()
        self._active = False

    def argument_handler(self, args):
        """
        Handles command-line arguments.
        """
        pass

    def interrupt_handler(self):
        """
        Handles a keyboard interrupt in the input loop.
        """
        self.stop()

    def start(self):
        """
        Starts the menu input loop.
        Commands will be processed and handled.
        """
        self._active = True
        session = PromptSession(history=FileHistory('.evillimiter_history'))
        html_completer = NestedCompleter.from_nested_dict(self.commands)
        while self._active:
            try:
                command = session.prompt(self.prompt, completer=html_completer, auto_suggest=AutoSuggestFromHistory())
            except KeyboardInterrupt:
                self.interrupt_handler()
                break

            # split command by spaces and parse the arguments
            parsed_args = self.parser.parse(command.split())
            if parsed_args is not None:
                self.argument_handler(parsed_args)

    def stop(self):
        """
        Breaks the menu input loop
        """
        self._active = False
