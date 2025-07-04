class ThemeNotFoundError(Exception):
    """Exception raised when specified theme file cannot be found.

    Attributes:
        message: Explanation of the error
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message
