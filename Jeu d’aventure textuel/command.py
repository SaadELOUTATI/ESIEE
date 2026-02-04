"""Command parsing helpers for player input."""

# This file contains the Command class.

class Command:
    """
    This class represents a command. A command is composed of a command word, a help
    string, an action and a number of parameters.

    Attributes:
        command_word (str): The command word.
        help_string (str): The help string.
        action (function): The action to execute when the command is called.
        number_of_parameters (int): The number of parameters expected by the command.

    Methods:
        __init__(self, command_word, help_string, action, number_of_parameters) : The constructor.
        __str__(self) : The string representation of the command.

    Examples:

    >>> from actions import go
    >>> command = Command("go", "Permet de se déplacer dans une direction.", go, 1)
    >>> command.command_word
    'go'
    >>> command.help_string
    'Permet de se déplacer dans une direction.'
    >>> type(command.action)
    <class 'function'>
    >>> command.number_of_parameters
    1

    """

    # The constructor.
    def __init__(self, command_word, help_string, action, number_of_parameters):
        self.command_word = command_word
        self.help_string = help_string
        self.action = action
        self.number_of_parameters = number_of_parameters

    # The string representation of the command.
    def __str__(self):
        return f"{self.command_word}{self.help_string}"

    def as_help_line(self):
        """Return the help line used when listing available commands."""
        return str(self)


def parse_quest_id(list_of_words):
    """
    Parse a numeric quest id from a command word list.
    Returns an int or None if not a valid id.
    """
    if len(list_of_words) != 2:
        return None
    if list_of_words[1].isdigit():
        return int(list_of_words[1])
    return None


def parse_context_index(list_of_words):
    """
    Parse a numeric index from a command word list.
    Returns an int or None if not a valid index.
    """
    if len(list_of_words) != 2:
        return None
    if list_of_words[1].isdigit():
        return int(list_of_words[1])
    return None


def parse_status(list_of_words):
    """
    Parse the status command (no parameters expected).
    Returns True when the command is valid, False otherwise.
    """
    return len(list_of_words) == 1
