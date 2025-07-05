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