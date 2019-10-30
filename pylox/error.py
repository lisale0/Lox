"""
Errors
~~~~~~~~~~~~~~~~
"""


class LoxRuntimeError(RuntimeError):
    """
    Lox Runtime Error
    """
    def __init__(self, token=None, message=None):
        self.token = token
        self.message = message

    def __str__(self):
        return f"{self.message}\n[line {self.token.line}]"
