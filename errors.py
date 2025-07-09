class DevlogError(Exception):
    """Base Class for all Devlog errors"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class ThemeNotFoundError(DevlogError):
    """Exception raised when specified theme file cannot be found.

    Attributes:
        message: Explanation of the error
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class CommandError(DevlogError):
    """Exception raised when a command encounters undefined"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class GitNotFoundError(DevlogError):
    """Exception raised when a git repository cannot be found in current directory"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class InvalidLocationError(DevlogError):
    """Exception raised when invalid location option is specified in grep command"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
